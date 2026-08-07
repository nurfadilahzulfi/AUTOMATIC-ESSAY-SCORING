import json
import logging

import httpx
from celery import shared_task
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """Kamu adalah penilai ujian esai akademik yang sangat ketat, adil, dan objektif.

Soal: {pertanyaan}
Referensi Jawaban (Kunci): {referensi_jawaban}
Kata Kunci Penting: {kata_kunci}

Jawaban Mahasiswa: {teks_jawaban}

Instruksi Penilaian Penting:
1. Periksa terlebih dahulu apakah jawaban mahasiswa koheren (masuk akal) dan menggunakan kata-kata yang valid. Jika jawaban berupa teks acak, ketikan asal-asalan (gibberish/random text seperti "asdasd", "lahfjashf"), tidak bermakna, tidak relevan sama sekali, atau hanya menyalin soal, Anda WAJIB memberikan Nilai 0 dengan alasan "Jawaban tidak valid, acak, atau tidak relevan".
2. Jangan memberikan Nilai 5 hanya karena jawaban "tidak lengkap". Nilai 5 hanya diberikan jika jawaban mahasiswa memiliki makna atau konsep yang relevan sebagian dengan referensi jawaban. Jika sama sekali tidak ada konsep yang benar atau jawaban ngasal, berikan Nilai 0.

Kriteria Penilaian:
- Nilai 10: Jawaban lengkap, benar, logis, dan mencakup semua aspek kunci dari referensi jawaban.
- Nilai 5: Jawaban memiliki poin/konsep yang sebagian benar dan relevan dengan referensi jawaban, tetapi kurang lengkap atau ada beberapa poin penting yang terlewat.
- Nilai 0: Jawaban salah total, berupa teks acak/asal-asalan, tidak relevan, kosong, atau hanya menyalin soal.

Balas HANYA dalam format JSON berikut, tanpa teks tambahan:
{{"nilai": <0|5|10>, "alasan": "<penjelasan singkat dalam Bahasa Indonesia, maksimal 2 kalimat>"}}"""


def _call_ollama(prompt: str) -> dict:
    """Kirim prompt ke Ollama dan kembalikan response JSON."""
    base_url = settings.OLLAMA_BASE_URL
    model = settings.OLLAMA_MODEL

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1,  # Rendah agar konsisten
            "num_predict": 200,
        },
    }

    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(f"{base_url}/api/generate", json=payload)
            response.raise_for_status()
            result = response.json()
            text = result.get("response", "").strip()
            return json.loads(text)
    except httpx.TimeoutException:
        logger.error("Ollama timeout saat menilai jawaban.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Gagal parse JSON dari Ollama: {e}")
        return None
    except Exception as e:
        logger.error(f"Error saat memanggil Ollama: {e}")
        return None


def _validate_nilai(nilai) -> int:
    """Pastikan nilai hanya 0, 5, atau 10."""
    try:
        n = int(nilai)
        if n in [0, 5, 10]:
            return n
        # Bulatkan ke yang terdekat
        if n <= 2:
            return 0
        elif n <= 7:
            return 5
        else:
            return 10
    except (TypeError, ValueError):
        return 0


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def grade_jawaban_task(self, jawaban_pk: int):
    """
    Celery task untuk menilai satu jawaban esai menggunakan LLM Ollama.
    Nilai: 0, 5, atau 10.
    """
    from apps.submissions.models import Jawaban

    try:
        jawaban = Jawaban.objects.select_related('soal', 'sesi__ujian').get(pk=jawaban_pk)
    except Jawaban.DoesNotExist:
        logger.error(f"Jawaban {jawaban_pk} tidak ditemukan.")
        return

    # Tandai sedang diproses
    jawaban.grading_status = Jawaban.GRADING_PROCESSING
    jawaban.save(update_fields=['grading_status'])

    # Jika jawaban kosong, langsung nilai 0
    if not jawaban.teks_jawaban.strip():
        jawaban.nilai = 0
        jawaban.alasan_nilai = "Jawaban kosong — mahasiswa tidak memberikan jawaban."
        jawaban.grading_status = Jawaban.GRADING_DONE
        jawaban.graded_at = timezone.now()
        jawaban.save()
        _cek_dan_update_total(jawaban.sesi)
        return

    soal = jawaban.soal
    prompt = PROMPT_TEMPLATE.format(
        pertanyaan=soal.pertanyaan,
        referensi_jawaban=soal.referensi_jawaban,
        kata_kunci=soal.kata_kunci or 'Tidak ada kata kunci tambahan.',
        teks_jawaban=jawaban.teks_jawaban,
    )

    result = _call_ollama(prompt)

    if result is None:
        # Retry jika gagal
        try:
            raise self.retry()
        except self.MaxRetriesExceededError:
            jawaban.grading_status = Jawaban.GRADING_FAILED
            jawaban.alasan_nilai = "Penilaian AI gagal setelah beberapa percobaan. Perlu penilaian manual."
            jawaban.save()
            return

    nilai = _validate_nilai(result.get('nilai', 0))
    alasan = result.get('alasan', 'Tidak ada keterangan.')

    jawaban.nilai = nilai
    jawaban.alasan_nilai = alasan
    jawaban.grading_status = Jawaban.GRADING_DONE
    jawaban.graded_at = timezone.now()
    jawaban.save()

    logger.info(f"Jawaban {jawaban_pk} dinilai: {nilai} — {alasan}")

    # Cek apakah semua soal sudah dinilai → update total nilai sesi
    _cek_dan_update_total(jawaban.sesi)


@shared_task
def grade_sesi_task(sesi_pk: int):
    """
    Task utama yang memicu penilaian semua jawaban dalam satu sesi ujian.
    Dipanggil setelah mahasiswa submit.
    """
    from apps.submissions.models import SesiUjian, Jawaban

    try:
        sesi = SesiUjian.objects.get(pk=sesi_pk)
    except SesiUjian.DoesNotExist:
        logger.error(f"Sesi {sesi_pk} tidak ditemukan.")
        return

    jawaban_list = sesi.jawaban.all()
    for jawaban in jawaban_list:
        grade_jawaban_task.delay(jawaban.pk)

    logger.info(f"Memulai penilaian {jawaban_list.count()} jawaban untuk sesi {sesi_pk}.")


def _cek_dan_update_total(sesi):
    """Update total nilai sesi jika semua jawaban sudah selesai dinilai."""
    from apps.submissions.models import Jawaban

    semua_jawaban = sesi.jawaban.all()
    if not semua_jawaban.filter(grading_status__in=[Jawaban.GRADING_PENDING, Jawaban.GRADING_PROCESSING]).exists():
        total = sum(j.nilai or 0 for j in semua_jawaban)
        sesi.total_nilai = total
        sesi.save(update_fields=['total_nilai'])
        logger.info(f"Sesi {sesi.pk} selesai dinilai. Total nilai: {total}")
