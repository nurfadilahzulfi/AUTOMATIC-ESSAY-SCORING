import json
import logging
import re

import httpx
from celery import shared_task
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Kamu adalah Dosen Penilai Ujian Esai Akademik yang adil, cermat, dan berwawasan.
Tugas kamu adalah menilai jawaban esai mahasiswa berdasarkan kunci jawaban yang diberikan.
Kamu HANYA boleh memberikan nilai 0, 5, atau 10.
Kamu HARUS merespons dalam format JSON murni tanpa markdown block."""

USER_PROMPT_TEMPLATE = """SOAL: {pertanyaan}
KUNCI JAWABAN: {referensi_jawaban}
KATA KUNCI PENTING: {kata_kunci}

JAWABAN MAHASISWA: {teks_jawaban}

ATURAN SKOR & KRITERIA PENILAIAN:
1. NILAI 10 (SEMPURNA / LENGKAP):
   - Jawaban memuat penjelasan konsep utama DAN contoh/detail teknis yang SEBAGIAN BESAR sesuai kunci jawaban.
   - PRINSIP FLEKSIBILITAS ILMIAH: Kunci jawaban dan kata kunci adalah panduan utama. Jika mahasiswa menggunakan penjelasan ilmiah alternatif, sinonim yang valid, atau contoh algoritma/teknik lain yang secara teori Machine Learning BENAR dan TEPAT (misal menyebut Random Forest/DBSCAN padahal kunci menyebut Linear Regression/K-Means), jawaban TETAP SAH dan berhak mendapat nilai 10.
   - Tidak perlu 100% menggunakan kata yang sama persis dengan kunci jawaban selama esensi ilmunya benar dan lengkap.

2. NILAI 5 (SEBAGIAN BENAR / KONSEPTUAL):
   - Mahasiswa memberikan DEFINISI DASAR ATAU PENJELASAN KONSEP INTI YANG BENAR dan RELEVAN dalam bentuk KALIMAT UTUH.
   - Contoh jawaban yang layak nilai 5: "ML adalah cabang kecerdasan buatan yang membuat komputer belajar dari data" (ada definisi/penjelasan yang benar).
   - Jawaban yang benar secara konsep dasar TIDAK BOLEH diberi nilai 0.
   - PENTING: Untuk mendapat nilai 5, jawaban HARUS berisi PENJELASAN atau DEFINISI dalam kalimat utuh. Hanya menyebutkan istilah/kata kunci saja TIDAK CUKUP.

3. NILAI 0 (SALAH / TIDAK RELEVAN / NON-SERIUS):
   - Jawaban salah total, acak (gibberish), kosong, candaan/troll, atau kalimat asal-asalan tanpa penjelasan teknis sama sekali.
   - Contoh jawaban bernilai 0: "pentinglah pokoknya", "karena penting", "ya begitu", "gatau", "feature gatau", "regression aja".
   - Jawaban yang hanya mengulang kata dari soal tanpa penjelasan ilmiah WAJIB diberi nilai 0.
   - Jawaban yang mengandung ungkapan ketidaktahuan ("gatau", "tidak tahu", "gak paham", "entahlah") WAJIB diberi nilai 0 meskipun ada kata kunci di dalamnya.
   - Jawaban yang HANYA menyebutkan istilah/kata kunci TANPA kalimat penjelasan (misal: "feature", "supervised", "regression") WAJIB diberi nilai 0.

Tuliskan "alasan" penilaian dalam 2-3 kalimat yang ramah, jujur, dan edukatif, lalu tentukan "nilai" (0, 5, atau 10).

OUTPUT FORMAT JSON:
{{"alasan": "<penjelasan>", "nilai": <0 atau 5 atau 10>}}
/no_think"""


def _clean_and_parse_json(text: str) -> dict:
    """Extract JSON object from raw response text (handles markdown, reasoning tags, etc.)."""
    if not text:
        return None

    # 1. Hapus tag <think>...</think> (Qwen3 / DeepSeek R1 reasoning models)
    # Juga handle <think> yang tidak tertutup (model kehabisan token saat reasoning)
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    cleaned = re.sub(r'<think>.*', '', cleaned, flags=re.DOTALL).strip()

    # 2. Hapus markdown codeblock ```json ... ``` jika ada
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'\s*```$', '', cleaned, flags=re.MULTILINE).strip()

    # 3. Try direct JSON parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 4. Extract first {...} pattern using regex
    match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def _call_ollama(prompt: str) -> dict:
    """Kirim prompt ke Ollama via Chat API dan kembalikan response JSON."""
    base_url = settings.OLLAMA_BASE_URL
    model = settings.OLLAMA_MODEL

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 1500,
            "top_k": 20,
            "top_p": 0.95,
        },
    }

    try:
        # Timeout 3600 detik (1 jam) sebagai safety ceiling.
        with httpx.Client(timeout=3600.0) as client:
            response = client.post(f"{base_url}/api/chat", json=payload)
            response.raise_for_status()
            result = response.json()
            text = result.get("message", {}).get("content", "").strip()
            logger.info(f"Ollama raw response ({model}): {text[:200]}...")
            parsed = _clean_and_parse_json(text)
            if parsed is None:
                logger.error(f"Gagal parse JSON dari Ollama raw text: {text[:200]}")
            return parsed
    except httpx.TimeoutException:
        logger.warning("Ollama timeout (>1 jam) — server kemungkinan crash atau tidak merespons sama sekali.")
        return None
    except Exception as e:
        logger.error(f"Error saat memanggil Ollama: {e}")
        return None


def _validate_nilai(nilai) -> int:
    """Pastikan nilai 0, 5, atau 10."""
    try:
        n = float(nilai)
        if n in [0, 5, 10]:
            return int(n)
        if n > 10:
            if n >= 75:
                return 10
            elif n >= 40:
                return 5
            else:
                return 0
        if n <= 2.5:
            return 0
        elif n <= 7.5:
            return 5
        else:
            return 10
    except (TypeError, ValueError):
        return 0


_EMBEDDING_MODEL = None


def _get_embedding_model():
    """Load dan cache model sentence-transformers di memori."""
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading sentence-transformers model 'paraphrase-multilingual-MiniLM-L12-v2'...")
            _EMBEDDING_MODEL = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        except Exception as e:
            logger.error(f"Error loading SentenceTransformer: {e}")
            return None
    return _EMBEDDING_MODEL


def calculate_embedding(text: str) -> list:
    """Hitung vektor embedding dari teks."""
    if not text or not text.strip():
        return None
    model = _get_embedding_model()
    if model is None:
        return None
    try:
        vec = model.encode(text.strip(), convert_to_numpy=True)
        return vec.tolist()
    except Exception as e:
        logger.error(f"Error calculating embedding: {e}")
        return None


def compute_cosine_similarity(vec1: list, vec2: list) -> float:
    """Hitung Cosine Similarity antara 2 vektor (0.00 - 1.00)."""
    if not vec1 or not vec2:
        return 0.0
    import numpy as np
    a = np.array(vec1)
    b = np.array(vec2)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    similarity = float(np.dot(a, b) / (norm_a * norm_b))
    return max(0.0, min(1.0, similarity))


def similarity_to_score(similarity: float) -> int:
    if similarity >= 0.75:
        return 10
    elif similarity >= 0.45:
        return 5
    else:
        return 0


@shared_task
def cache_soal_embedding_task(soal_pk: int):
    """Pre-compute dan simpan embedding referensi_jawaban pada model Soal."""
    from apps.exams.models import Soal
    try:
        soal = Soal.objects.get(pk=soal_pk)
        if soal.referensi_jawaban:
            vec = calculate_embedding(soal.referensi_jawaban)
            if vec:
                soal.referensi_embedding = vec
                soal.save(update_fields=['referensi_embedding'])
                logger.info(f"Embedding cache berhasil disimpan untuk Soal ID {soal_pk}.")
    except Soal.DoesNotExist:
        logger.error(f"Soal {soal_pk} tidak ditemukan.")
    except Exception as e:
        logger.error(f"Gagal menghitung embedding Soal {soal_pk}: {e}")


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    soft_time_limit=3700,   # Celery soft kill di 61 menit 40 detik (log warning)
    time_limit=4200,        # Celery hard kill di 70 menit (absolute safety net)
)
def grade_jawaban_task(self, jawaban_pk: int):
    """
    Celery task untuk menilai satu jawaban esai menggunakan LLM Ollama.
    Menghasilkan skor (0, 5, 10) dan alasan analisis mendetail.
    """
    from apps.submissions.models import Jawaban

    try:
        jawaban = Jawaban.objects.select_related('soal', 'sesi__ujian').get(pk=jawaban_pk)
    except Jawaban.DoesNotExist:
        logger.error(f"Jawaban {jawaban_pk} tidak ditemukan.")
        return

    jawaban.grading_status = Jawaban.GRADING_PROCESSING
    jawaban.save(update_fields=['grading_status'])

    if not jawaban.teks_jawaban.strip():
        jawaban.nilai = 0
        jawaban.similarity_score = 0.0
        jawaban.alasan_nilai = "Jawaban kosong — mahasiswa tidak memberikan jawaban."
        jawaban.grading_status = Jawaban.GRADING_DONE
        jawaban.graded_at = timezone.now()
        jawaban.save()
        _cek_dan_update_total(jawaban.sesi)
        return

    soal = jawaban.soal

    # Hitung similarity score jika model embedding tersedia
    similarity = 0.0
    ref_vec = soal.referensi_embedding
    if not ref_vec and soal.referensi_jawaban:
        ref_vec = calculate_embedding(soal.referensi_jawaban)
        if ref_vec:
            soal.referensi_embedding = ref_vec
            soal.save(update_fields=['referensi_embedding'])

    ans_vec = calculate_embedding(jawaban.teks_jawaban)
    if ref_vec and ans_vec:
        similarity = compute_cosine_similarity(ref_vec, ans_vec)

    jawaban.similarity_score = round(similarity, 4)
    embedding_nilai = similarity_to_score(similarity)

    prompt = USER_PROMPT_TEMPLATE.format(
        pertanyaan=soal.pertanyaan,
        referensi_jawaban=soal.referensi_jawaban,
        kata_kunci=soal.kata_kunci or 'Tidak ada kata kunci tambahan.',
        teks_jawaban=jawaban.teks_jawaban,
    )

    result = _call_ollama(prompt)

    if result is None:
        # Jika LLM timeout (antrean sangat penuh), retry dengan jeda 60 detik
        try:
            logger.warning(f"Ollama tidak merespons untuk jawaban {jawaban_pk}. Retry ke-{self.request.retries + 1}/3 dalam 60 detik...")
            raise self.retry(countdown=60)
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded untuk jawaban {jawaban_pk}. Fallback ke embedding score.")
            final_nilai = embedding_nilai
            alasan = ""
    else:
        raw_nilai = result.get('nilai') if result.get('nilai') is not None else result.get('skor', result.get('score', None))
        final_nilai = _validate_nilai(raw_nilai) if raw_nilai is not None else embedding_nilai
        raw_alasan = (
            result.get('alasan') or
            result.get('reason') or
            result.get('explanation') or
            result.get('analisis') or
            result.get('feedback') or
            result.get('keterangan') or
            result.get('alasan_penilaian') or
            ''
        )
        alasan = str(raw_alasan).strip()

    if not alasan:
        if final_nilai == 10:
            alasan = "Jawaban sudah tepat dan berhasil menjelaskan konsep utama secara akurat sesuai kunci jawaban."
        elif final_nilai == 5:
            alasan = "Jawaban sudah cukup baik dan relevan, namun penjelasan atau contoh yang diminta masih kurang lengkap."
        else:
            alasan = "Jawaban belum menjawab inti pertanyaan atau belum sesuai dengan materi pada kunci jawaban."

    jawaban.nilai = final_nilai
    jawaban.alasan_nilai = alasan
    jawaban.grading_status = Jawaban.GRADING_DONE
    jawaban.graded_at = timezone.now()
    jawaban.save()

    logger.info(f"Jawaban {jawaban_pk} dinilai ({settings.OLLAMA_MODEL}): {final_nilai} — {alasan}")
    _cek_dan_update_total(jawaban.sesi)


@shared_task
def grade_sesi_task(sesi_pk: int):
    """
    Task utama yang memicu penilaian semua jawaban dalam satu sesi ujian.
    Dipanggil setelah mahasiswa submit. Membagi antrean secara bertahap agar Ollama tidak overload.
    """
    from apps.submissions.models import SesiUjian, Jawaban

    try:
        sesi = SesiUjian.objects.get(pk=sesi_pk)
    except SesiUjian.DoesNotExist:
        logger.error(f"Sesi {sesi_pk} tidak ditemukan.")
        return

    jawaban_list = sesi.jawaban.all()
    for idx, jawaban in enumerate(jawaban_list):
        # Beri jeda 2 detik antar soal agar antrean Ollama teratur tanpa terjadi bottleneck
        grade_jawaban_task.apply_async(args=[jawaban.pk], countdown=idx * 2)

    logger.info(f"Memulai penilaian {jawaban_list.count()} jawaban bertahap untuk sesi {sesi_pk}.")


def _cek_dan_update_total(sesi):
    """Update total nilai sesi jika semua jawaban sudah selesai dinilai."""
    from apps.submissions.models import Jawaban

    semua_jawaban = sesi.jawaban.all()
    if not semua_jawaban.filter(grading_status__in=[Jawaban.GRADING_PENDING, Jawaban.GRADING_PROCESSING]).exists():
        total = sum(j.nilai or 0 for j in semua_jawaban)
        sesi.total_nilai = total
        sesi.save(update_fields=['total_nilai'])
        logger.info(f"Sesi {sesi.pk} selesai dinilai. Total nilai: {total}")
