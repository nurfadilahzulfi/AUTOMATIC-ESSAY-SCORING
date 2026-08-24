from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.exams.models import Ujian
from .models import SesiUjian, Jawaban
from .serializers import SesiUjianSerializer


class MulaiUjianView(APIView):
    """
    POST /api/v1/submission/mulai/<ujian_pk>/
    Mahasiswa memulai atau melanjutkan sesi ujian.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, ujian_pk):
        if not request.user.is_mahasiswa:
            return Response({'detail': 'Akses ditolak.'}, status=403)
        if request.user.is_exam_locked:
            return Response({'detail': 'Akun Anda dikunci karena pelanggaran ujian.', 'locked': True}, status=403)

        ujian = get_object_or_404(Ujian, pk=ujian_pk, status=Ujian.STATUS_AKTIF)

        # Validasi kelas
        if request.user.kelas not in ujian.get_kelas_list():
            return Response({'detail': 'Anda tidak terdaftar untuk ujian ini.'}, status=403)

        # Buat atau ambil sesi yang sudah ada (re-login support)
        sesi, created = SesiUjian.objects.get_or_create(
            mahasiswa=request.user,
            ujian=ujian,
            defaults={
                'status': SesiUjian.STATUS_BERLANGSUNG,
                'ip_address': request.META.get('REMOTE_ADDR'),
            }
        )

        if sesi.status == SesiUjian.STATUS_SELESAI:
            return Response({'detail': 'Ujian sudah selesai.', 'sesi_id': sesi.pk, 'selesai': True})
        if sesi.status == SesiUjian.STATUS_PELANGGARAN:
            return Response({'detail': 'Sesi dihentikan karena pelanggaran.', 'locked': True}, status=403)

        # Buat jawaban kosong untuk semua soal jika belum ada
        for soal in ujian.soal.all():
            Jawaban.objects.get_or_create(sesi=sesi, soal=soal)

        # Hitung sisa waktu
        elapsed = (timezone.now() - sesi.waktu_mulai).total_seconds()
        sisa_detik = max(0, (ujian.durasi_menit * 60) - int(elapsed))

        return Response({
            'sesi_id': sesi.pk,
            'dibuat_baru': created,
            'sisa_detik': sisa_detik,
            'waktu_mulai': sesi.waktu_mulai,
        })


class SesiUjianDetailView(APIView):
    """
    GET /api/v1/submission/sesi/<sesi_pk>/
    Ambil detail sesi ujian beserta soal dan jawaban saat ini.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, sesi_pk):
        if request.user.is_mahasiswa:
            sesi = get_object_or_404(SesiUjian, pk=sesi_pk, mahasiswa=request.user)
        else:
            sesi = get_object_or_404(SesiUjian, pk=sesi_pk)

        elapsed = (timezone.now() - sesi.waktu_mulai).total_seconds()
        sisa_detik = max(0, (sesi.ujian.durasi_menit * 60) - int(elapsed))

        from apps.exams.serializers import UjianMahasiswaSerializer
        data = SesiUjianSerializer(sesi).data
        data['sisa_detik'] = sisa_detik
        return Response(data)


class SaveJawabanView(APIView):
    """
    POST /api/v1/submission/save-jawaban/
    Auto-save jawaban mahasiswa (dipanggil periodik dari frontend).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sesi_pk = request.data.get('sesi_pk')
        soal_id = request.data.get('soal_id')
        teks = request.data.get('teks_jawaban', '').strip()

        sesi = get_object_or_404(SesiUjian, pk=sesi_pk, mahasiswa=request.user)
        if sesi.status != SesiUjian.STATUS_BERLANGSUNG:
            return Response({'detail': 'Sesi tidak aktif.'}, status=400)

        # Cek timeout waktu ujian
        elapsed = (timezone.now() - sesi.waktu_mulai).total_seconds()
        if elapsed > sesi.ujian.durasi_menit * 60:
            return Response({'detail': 'Waktu ujian telah habis.', 'timeout': True}, status=400)

        jawaban = get_object_or_404(Jawaban, sesi=sesi, soal_id=soal_id)
        jawaban.teks_jawaban = teks
        jawaban.save(update_fields=['teks_jawaban'])
        return Response({'status': 'ok', 'soal_id': soal_id})


class SubmitUjianView(APIView):
    """
    POST /api/v1/submission/submit/<sesi_pk>/
    Submit ujian — trigger Celery grading.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, sesi_pk):
        sesi = get_object_or_404(SesiUjian, pk=sesi_pk, mahasiswa=request.user)

        if sesi.status == SesiUjian.STATUS_SELESAI:
            return Response({'detail': 'Ujian sudah disubmit sebelumnya.', 'sesi_id': sesi.pk})

        with transaction.atomic():
            sesi.status = SesiUjian.STATUS_SELESAI
            sesi.waktu_selesai = timezone.now()
            sesi.save()

        # Trigger Celery grading task
        from apps.grading.tasks import grade_sesi_task
        grade_sesi_task.delay(sesi.pk)

        return Response({
            'detail': 'Ujian berhasil disubmit. Penilaian AI sedang diproses.',
            'sesi_id': sesi.pk,
        })


class HasilUjianView(APIView):
    """
    GET /api/v1/submission/hasil/<sesi_pk>/
    Hasil ujian — nilai per soal dan total (polling sampai grading selesai).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, sesi_pk):
        if request.user.is_mahasiswa:
            sesi = get_object_or_404(SesiUjian, pk=sesi_pk, mahasiswa=request.user)
        else:
            sesi = get_object_or_404(SesiUjian, pk=sesi_pk)

        jawaban_list = sesi.jawaban.all().select_related('soal').order_by('soal__nomor_urut')
        # Selesai dinilai jika tidak ada lagi yang statusnya pending atau processing
        semua_selesai = not jawaban_list.filter(grading_status__in=[Jawaban.GRADING_PENDING, Jawaban.GRADING_PROCESSING]).exists()

        return Response({
            'sesi_id': sesi.pk,
            'status': sesi.status,
            'total_nilai': sesi.total_nilai,
            'nilai_maksimal': sesi.ujian.nilai_maksimal,
            'semua_selesai_dinilai': semua_selesai,
            'jawaban': [
                {
                    'nomor_soal': j.soal.nomor_urut,
                    'pertanyaan': j.soal.pertanyaan,
                    'teks_jawaban': j.teks_jawaban,
                    'nilai': j.nilai,
                    'alasan_nilai': j.alasan_nilai,
                    'grading_status': j.grading_status,
                }
                for j in jawaban_list
            ],
        })


class RiwayatUjianView(APIView):
    """
    GET /api/v1/submission/riwayat/
    Daftar seluruh riwayat sesi ujian mahasiswa (selesai & pelanggaran).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_mahasiswa:
            return Response({'detail': 'Akses ditolak.'}, status=403)

        sesi_qs = SesiUjian.objects.filter(
            mahasiswa=request.user,
            status__in=[SesiUjian.STATUS_SELESAI, SesiUjian.STATUS_PELANGGARAN]
        ).select_related('ujian', 'ujian__mata_pelajaran').order_by('-waktu_mulai')

        result = []
        for s in sesi_qs:
            u = s.ujian
            result.append({
                'id': u.id,
                'sesi_id': s.id,
                'judul': u.judul,
                'mata_pelajaran': u.mata_pelajaran.nama if u.mata_pelajaran else '—',
                'durasi_menit': u.durasi_menit,
                'jumlah_soal': u.jumlah_soal,
                'nilai_maksimal': u.nilai_maksimal,
                'total_nilai': s.total_nilai,
                'tanggal_ujian': s.waktu_mulai.strftime('%d %b %Y, %H:%M') if s.waktu_mulai else (u.tanggal_ujian or '—'),
                'status_sesi': s.status,
                'semua_selesai_dinilai': s.semua_selesai_dinilai,
            })
        return Response(result)

