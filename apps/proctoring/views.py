import json
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.submissions.models import SesiUjian
from .models import HeartbeatLog, PelanggaranLog


class HeartbeatView(APIView):
    """
    POST /api/v1/proctoring/heartbeat/
    Dipanggil frontend setiap 15 detik selama ujian berlangsung.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sesi_pk = request.data.get('sesi_pk')
        if not sesi_pk:
            return Response({'detail': 'sesi_pk wajib diisi.'}, status=400)

        sesi = get_object_or_404(SesiUjian, pk=sesi_pk, mahasiswa=request.user)
        if sesi.status != SesiUjian.STATUS_BERLANGSUNG:
            return Response({'status': 'sesi_berakhir', 'sesi_status': sesi.status})

        now = timezone.now()
        sesi.last_heartbeat = now
        sesi.save(update_fields=['last_heartbeat'])
        HeartbeatLog.objects.create(sesi=sesi)

        # Hitung sisa waktu ujian
        elapsed = (now - sesi.waktu_mulai).total_seconds()
        sisa_detik = max(0, (sesi.ujian.durasi_menit * 60) - int(elapsed))

        return Response({
            'status': 'ok',
            'sisa_detik': sisa_detik,
            'server_time': now.isoformat(),
        })


class CatatPelanggaranView(APIView):
    """
    POST /api/v1/proctoring/pelanggaran/
    Mencatat pelanggaran dan mengunci akun mahasiswa (zero tolerance).

    Tipe pelanggaran yang diterima:
    - tab_baru
    - window_blur
    - fullscreen_exit
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sesi_pk = request.data.get('sesi_pk')
        tipe = request.data.get('tipe')
        keterangan = request.data.get('keterangan', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        TIPE_VALID = [t[0] for t in PelanggaranLog.TIPE_CHOICES]
        if tipe not in TIPE_VALID:
            return Response({'detail': f"Tipe pelanggaran tidak valid. Pilihan: {TIPE_VALID}"}, status=400)

        sesi = get_object_or_404(SesiUjian, pk=sesi_pk, mahasiswa=request.user)
        if sesi.status != SesiUjian.STATUS_BERLANGSUNG:
            return Response({'status': 'sesi_sudah_berakhir', 'sesi_status': sesi.status})

        # Catat log
        PelanggaranLog.objects.create(
            sesi=sesi,
            tipe=tipe,
            keterangan=keterangan,
            user_agent=user_agent,
        )

        # Zero tolerance — langsung kunci dan akhiri sesi
        sesi.status = SesiUjian.STATUS_PELANGGARAN
        sesi.waktu_selesai = timezone.now()
        sesi.save()

        mahasiswa = sesi.mahasiswa
        mahasiswa.is_exam_locked = True
        mahasiswa.lock_reason = (
            f"Pelanggaran terdeteksi: {tipe.replace('_', ' ').title()} "
            f"pada ujian '{sesi.ujian.judul}' "
            f"pukul {timezone.now().strftime('%H:%M:%S WIB')}."
        )
        mahasiswa.locked_at = timezone.now()
        mahasiswa.save()

        return Response({
            'status': 'pelanggaran_tercatat',
            'detail': 'Sesi Anda dihentikan karena pelanggaran. Akun dikunci.',
            'tipe': tipe,
        }, status=200)
