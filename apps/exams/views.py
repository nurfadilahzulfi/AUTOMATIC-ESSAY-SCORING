import openpyxl
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg

from .models import MataPelajaran, Ujian, Soal
from .serializers import (
    MataPelajaranSerializer, UjianSerializer,
    UjianDetailSerializer, UjianMahasiswaSerializer, SoalSerializer,
)


def require_dosen(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_dosen:
            return Response({'detail': 'Akses ditolak. Hanya dosen.'}, status=403)
        return func(self, request, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

class DashboardDosenView(APIView):
    """GET /api/v1/ujian/dashboard/"""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def get(self, request):
        from apps.submissions.models import SesiUjian
        ujian_qs = Ujian.objects.filter(mata_pelajaran__dosen=request.user)
        return Response({
            'total_ujian': ujian_qs.count(),
            'ujian_draft': ujian_qs.filter(status=Ujian.STATUS_DRAFT).count(),
            'ujian_aktif': ujian_qs.filter(status=Ujian.STATUS_AKTIF).count(),
            'ujian_selesai': ujian_qs.filter(status=Ujian.STATUS_SELESAI).count(),
            'total_peserta': SesiUjian.objects.filter(ujian__mata_pelajaran__dosen=request.user).count(),
            'ujian_terbaru': UjianSerializer(ujian_qs.order_by('-created_at')[:5], many=True).data,
        })


# ─────────────────────────────────────────────────────────────────────────────
# MATA PELAJARAN
# ─────────────────────────────────────────────────────────────────────────────

class MataPelajaranListCreateView(APIView):
    """GET, POST /api/v1/ujian/mata-kuliah/"""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def get(self, request):
        qs = MataPelajaran.objects.filter(dosen=request.user)
        return Response(MataPelajaranSerializer(qs, many=True).data)

    @require_dosen
    def post(self, request):
        serializer = MataPelajaranSerializer(data=request.data)
        if serializer.is_valid():
            kode = serializer.validated_data['kode'].upper()
            if MataPelajaran.objects.filter(kode=kode).exists():
                return Response({'detail': f"Kode '{kode}' sudah digunakan."}, status=400)
            serializer.save(dosen=request.user, kode=kode)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MataPelajaranDetailView(APIView):
    """DELETE /api/v1/ujian/mata-kuliah/<pk>/"""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def delete(self, request, pk):
        mp = get_object_or_404(MataPelajaran, pk=pk, dosen=request.user)
        mp.delete()
        return Response({'detail': 'Mata pelajaran berhasil dihapus.'})


# ─────────────────────────────────────────────────────────────────────────────
# UJIAN
# ─────────────────────────────────────────────────────────────────────────────

class UjianListCreateView(APIView):
    """GET, POST /api/v1/ujian/"""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def get(self, request):
        qs = Ujian.objects.filter(mata_pelajaran__dosen=request.user).select_related('mata_pelajaran')
        return Response(UjianSerializer(qs, many=True).data)

    @require_dosen
    def post(self, request):
        mp_id = request.data.get('mata_pelajaran')
        get_object_or_404(MataPelajaran, pk=mp_id, dosen=request.user)
        serializer = UjianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UjianDetailView(APIView):
    """GET, PUT, DELETE /api/v1/ujian/<pk>/"""
    permission_classes = [IsAuthenticated]

    def _get_ujian(self, pk, user):
        return get_object_or_404(Ujian, pk=pk, mata_pelajaran__dosen=user)

    @require_dosen
    def get(self, request, pk):
        ujian = self._get_ujian(pk, request.user)
        return Response(UjianDetailSerializer(ujian).data)

    @require_dosen
    def put(self, request, pk):
        ujian = self._get_ujian(pk, request.user)
        serializer = UjianSerializer(ujian, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @require_dosen
    def delete(self, request, pk):
        ujian = self._get_ujian(pk, request.user)
        judul = ujian.judul
        ujian.delete()
        return Response({'detail': f"Ujian '{judul}' berhasil dihapus."})


class AktivasiUjianView(APIView):
    """POST /api/v1/ujian/<pk>/aktivasi/"""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def post(self, request, pk):
        ujian = get_object_or_404(Ujian, pk=pk, mata_pelajaran__dosen=request.user)
        if ujian.jumlah_soal == 0:
            return Response({'detail': 'Ujian belum memiliki soal.'}, status=400)
        if ujian.status == Ujian.STATUS_DRAFT:
            ujian.status = Ujian.STATUS_AKTIF
            msg = f"Ujian '{ujian.judul}' sekarang AKTIF."
        elif ujian.status == Ujian.STATUS_AKTIF:
            ujian.status = Ujian.STATUS_SELESAI
            msg = f"Ujian '{ujian.judul}' telah DITUTUP."
        else:
            return Response({'detail': 'Ujian sudah selesai.'}, status=400)
        ujian.save()
        return Response({'detail': msg, 'status': ujian.status})


class MonitorUjianView(APIView):
    """GET /api/v1/ujian/<pk>/monitor/ — Live monitoring peserta ujian."""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def get(self, request, pk):
        from apps.submissions.models import SesiUjian
        from apps.submissions.serializers import SesiUjianListSerializer
        ujian = get_object_or_404(Ujian, pk=pk, mata_pelajaran__dosen=request.user)
        sesi_list = SesiUjian.objects.filter(ujian=ujian).select_related('mahasiswa').order_by('mahasiswa__kelas')
        return Response({
            'ujian': UjianSerializer(ujian).data,
            'peserta': SesiUjianListSerializer(sesi_list, many=True).data,
        })


# ─────────────────────────────────────────────────────────────────────────────
# SOAL
# ─────────────────────────────────────────────────────────────────────────────

class SoalListCreateView(APIView):
    """GET, POST /api/v1/ujian/<ujian_pk>/soal/"""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def get(self, request, ujian_pk):
        ujian = get_object_or_404(Ujian, pk=ujian_pk, mata_pelajaran__dosen=request.user)
        return Response(SoalSerializer(ujian.soal.order_by('nomor_urut'), many=True).data)

    @require_dosen
    def post(self, request, ujian_pk):
        ujian = get_object_or_404(Ujian, pk=ujian_pk, mata_pelajaran__dosen=request.user)
        nomor = ujian.soal.count() + 1
        data = {**request.data, 'nomor_urut': nomor}
        serializer = SoalSerializer(data=data)
        if serializer.is_valid():
            serializer.save(ujian=ujian)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SoalDetailView(APIView):
    """DELETE /api/v1/ujian/soal/<pk>/"""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def delete(self, request, pk):
        soal = get_object_or_404(Soal, pk=pk, ujian__mata_pelajaran__dosen=request.user)
        ujian = soal.ujian
        soal.delete()
        for i, s in enumerate(ujian.soal.order_by('nomor_urut'), 1):
            if s.nomor_urut != i:
                s.nomor_urut = i
                s.save(update_fields=['nomor_urut'])
        return Response({'detail': 'Soal berhasil dihapus.'})


class UploadSoalExcelView(APIView):
    """POST /api/v1/ujian/<ujian_pk>/soal/upload/"""
    permission_classes = [IsAuthenticated]

    @require_dosen
    def post(self, request, ujian_pk):
        ujian = get_object_or_404(Ujian, pk=ujian_pk, mata_pelajaran__dosen=request.user)
        excel_file = request.FILES.get('file_excel')
        if not excel_file:
            return Response({'detail': 'File Excel wajib dilampirkan.'}, status=400)
        try:
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            ujian.soal.all().delete()
            count = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row[0]:
                    continue
                Soal.objects.create(
                    ujian=ujian,
                    nomor_urut=int(row[0]),
                    pertanyaan=str(row[1]).strip(),
                    referensi_jawaban=str(row[2]).strip() if len(row) > 2 and row[2] else '',
                    kata_kunci=str(row[3]).strip() if len(row) > 3 and row[3] else '',
                )
                count += 1
            return Response({'detail': f'Berhasil mengimpor {count} soal.', 'jumlah_soal': count})
        except Exception as e:
            return Response({'detail': f'Gagal membaca file: {str(e)}'}, status=400)


# ─────────────────────────────────────────────────────────────────────────────
# MAHASISWA: Daftar ujian yang tersedia
# ─────────────────────────────────────────────────────────────────────────────

class UjianTersediaView(APIView):
    """
    GET /api/v1/ujian/tersedia/
    Daftar ujian aktif yang tersedia untuk mahasiswa berdasarkan kelasnya.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_mahasiswa:
            return Response({'detail': 'Akses ditolak.'}, status=403)
        from apps.submissions.models import SesiUjian
        ujian_list = Ujian.objects.filter(
            status=Ujian.STATUS_AKTIF,
            kelas_target__icontains=request.user.kelas,
        )
        sesi_map = {s.ujian_id: s.status for s in SesiUjian.objects.filter(mahasiswa=request.user)}
        result = []
        for u in ujian_list:
            result.append({
                'id': u.id,
                'judul': u.judul,
                'mata_pelajaran': u.mata_pelajaran.nama,
                'durasi_menit': u.durasi_menit,
                'jumlah_soal': u.jumlah_soal,
                'nilai_maksimal': u.nilai_maksimal,
                'tanggal_ujian': u.tanggal_ujian,
                'status_sesi': sesi_map.get(u.id, None),
            })
        return Response(result)
