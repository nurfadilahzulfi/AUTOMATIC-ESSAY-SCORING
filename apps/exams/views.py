import openpyxl
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db import transaction
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
        from django.utils import timezone
        from django.db.models import Avg, Count
        from apps.submissions.models import SesiUjian
        from apps.proctoring.models import PelanggaranLog

        ujian_qs = Ujian.objects.filter(mata_pelajaran__dosen=request.user)
        sesi_qs = SesiUjian.objects.filter(ujian__mata_pelajaran__dosen=request.user)

        ujian_aktif_count = ujian_qs.filter(status=Ujian.STATUS_AKTIF).count()
        ujian_selesai_count = ujian_qs.filter(status=Ujian.STATUS_SELESAI).count()
        total_sesi = sesi_qs.count()
        sesi_selesai = sesi_qs.filter(status=SesiUjian.STATUS_SELESAI).count()
        total_pelanggaran = PelanggaranLog.objects.filter(
            sesi__ujian__mata_pelajaran__dosen=request.user
        ).count()

        # Rata-rata nilai (hanya sesi selesai yang sudah dinilai)
        rata_avg = sesi_qs.filter(
            status=SesiUjian.STATUS_SELESAI,
            total_nilai__isnull=False
        ).aggregate(avg=Avg('total_nilai'))['avg']
        rata_rata_nilai = round(rata_avg, 1) if rata_avg is not None else 0.0

        # Persen selesai dan kelulusan
        persen_selesai = round((sesi_selesai / total_sesi * 100), 1) if total_sesi else 0
        sesi_lulus = sesi_qs.filter(
            status=SesiUjian.STATUS_SELESAI,
            total_nilai__gte=60
        ).count()
        persen_kelulusan = round((sesi_lulus / sesi_selesai * 100), 1) if sesi_selesai else 0

        # Chart keaktifan per bulan (12 bulan terakhir vs 12 bulan tahun sebelumnya)
        now = timezone.now()
        current_year = now.year
        prev_year = current_year - 1
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',
                        'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']

        def monthly_counts(year):
            counts = []
            for m in range(1, 13):
                c = sesi_qs.filter(
                    waktu_mulai__year=year,
                    waktu_mulai__month=m
                ).count()
                counts.append(c)
            return counts

        chart_keaktifan = {
            'current_year': monthly_counts(current_year),
            'previous_year': monthly_counts(prev_year),
            'labels': month_labels,
            'current_year_label': str(current_year),
            'previous_year_label': str(prev_year),
        }

        # Statistik topik (soal per mata kuliah)
        topik_qs = ujian_qs.values(
            'mata_pelajaran__nama', 'mata_pelajaran__kode'
        ).annotate(jumlah=Count('soal')).order_by('-jumlah')[:5]
        total_soal = sum(t['jumlah'] for t in topik_qs)
        topik_stats = []
        for t in topik_qs:
            topik_stats.append({
                'nama': t['mata_pelajaran__nama'],
                'kode': t['mata_pelajaran__kode'],
                'jumlah': t['jumlah'],
                'persen': round((t['jumlah'] / total_soal * 100), 1) if total_soal else 0,
            })

        # Live aktivitas (10 sesi terbaru)
        recent_sesi = sesi_qs.select_related('mahasiswa', 'ujian').order_by('-waktu_mulai')[:10]
        live_activities = []
        for s in recent_sesi:
            live_activities.append({
                'user': s.mahasiswa.nama_lengkap,
                'action': f"{s.ujian.judul[:30]}{'...' if len(s.ujian.judul) > 30 else ''}",
                'status': s.status,
                'time': s.waktu_mulai.isoformat() if s.waktu_mulai else None,
            })

        return Response({
            # Fields yang digunakan frontend dashboard
            'ujian_aktif': ujian_aktif_count,
            'ujian_selesai': ujian_selesai_count,
            'total_sesi': total_sesi,
            'total_pelanggaran': total_pelanggaran,
            'rata_rata_nilai': rata_rata_nilai,
            'total_soal': total_soal,
            'persen_selesai': persen_selesai,
            'persen_kelulusan': persen_kelulusan,
            'chart_keaktifan': chart_keaktifan,
            'topik_stats': topik_stats,
            'live_activities': live_activities,
            # Field lama (backward compat)
            'total_ujian': ujian_qs.count(),
            'ujian_draft': ujian_qs.filter(status=Ujian.STATUS_DRAFT).count(),
            'total_peserta': total_sesi,
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

class HentikanUjianView(APIView):
    """
    POST /api/v1/ujian/<pk>/hentikan/
    Dosen menghentikan ujian secara paksa untuk seluruh peserta.
 
    Beda dengan AktivasiUjianView (yang cuma toggle status Ujian):
    view ini SEKALIGUS memaksa semua SesiUjian yang masih
    'berlangsung' jadi 'selesai' dan otomatis dikirim ke Celery
    untuk dinilai — jawaban yang sudah tersimpan dari auto-save
    tetap ikut dinilai apa adanya.
    """
    permission_classes = [IsAuthenticated]
 
    @require_dosen
    def post(self, request, pk):
        # Pola ownership sama seperti UjianDetailView/AktivasiUjianView:
        # kepemilikan ujian lewat mata_pelajaran__dosen, bukan field
        # dosen langsung di Ujian.
        ujian = get_object_or_404(Ujian, pk=pk, mata_pelajaran__dosen=request.user)
 
        if ujian.status == Ujian.STATUS_SELESAI:
            return Response({
                'detail': 'Ujian sudah dihentikan sebelumnya.',
                'status': ujian.status,
            })
 
        from django.db import transaction
        from django.utils import timezone
        from apps.submissions.models import SesiUjian
        from apps.grading.tasks import grade_sesi_task
 
        with transaction.atomic():
            ujian.status = Ujian.STATUS_SELESAI
            ujian.save(update_fields=['status'])
 
            sesi_aktif = SesiUjian.objects.filter(
                ujian=ujian,
                status=SesiUjian.STATUS_BERLANGSUNG,
            )
            sesi_ids = list(sesi_aktif.values_list('pk', flat=True))
            sesi_aktif.update(
                status=SesiUjian.STATUS_SELESAI,
                waktu_selesai=timezone.now(),
            )
 
        # Trigger grading Celery untuk setiap sesi yang baru dipaksa selesai
        for sesi_id in sesi_ids:
            grade_sesi_task.delay(sesi_id)
 
        return Response({
            'detail': f"Ujian '{ujian.judul}' berhasil dihentikan. "
                      f"{len(sesi_ids)} sesi yang masih berlangsung otomatis "
                      f"disubmit dan dinilai.",
            'status': ujian.status,
            'jumlah_sesi_dihentikan': len(sesi_ids),
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
        from apps.grading.tasks import cache_soal_embedding_task
        ujian = get_object_or_404(Ujian, pk=ujian_pk, mata_pelajaran__dosen=request.user)
        nomor = ujian.soal.count() + 1
        data = {**request.data, 'nomor_urut': nomor}
        serializer = SoalSerializer(data=data)
        if serializer.is_valid():
            soal = serializer.save(ujian=ujian)
            # Trigger pre-compute embedding kunci jawaban secara async
            cache_soal_embedding_task.delay(soal.pk)
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
    parser_classes = [MultiPartParser, FormParser]

    @require_dosen
    def post(self, request, ujian_pk):
        ujian = get_object_or_404(Ujian, pk=ujian_pk, mata_pelajaran__dosen=request.user)
        excel_file = request.FILES.get('file_excel')
        if not excel_file:
            return Response({'detail': 'File Excel wajib dilampirkan.'}, status=400)
        try:
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active

            soal_to_create = []
            count = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                nomor_raw = row[0]
                if nomor_raw is None:
                    continue
                try:
                    nomor_urut = int(nomor_raw)
                except (ValueError, TypeError):
                    nomor_urut = count + 1

                pertanyaan = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ''
                if not pertanyaan or pertanyaan == 'None':
                    continue

                referensi = str(row[2]).strip() if len(row) > 2 and row[2] is not None else ''
                if referensi == 'None':
                    referensi = ''

                kata_kunci = str(row[3]).strip() if len(row) > 3 and row[3] is not None else ''
                if kata_kunci == 'None':
                    kata_kunci = ''

                soal_to_create.append(Soal(
                    ujian=ujian,
                    nomor_urut=nomor_urut,
                    pertanyaan=pertanyaan,
                    referensi_jawaban=referensi,
                    kata_kunci=kata_kunci,
                ))
                count += 1

            if not soal_to_create:
                return Response({'detail': 'Tidak ada soal valid yang ditemukan dalam file Excel. Pastikan baris ke-2 dst terisi.'}, status=400)

            with transaction.atomic():
                ujian.soal.all().delete()
                created_soal = Soal.objects.bulk_create(soal_to_create)

            # Trigger pre-compute embedding untuk setiap soal yang baru diimport
            from apps.grading.tasks import cache_soal_embedding_task
            for soal in ujian.soal.all():
                cache_soal_embedding_task.delay(soal.pk)

            return Response({'detail': f'Berhasil mengimpor {count} soal.', 'jumlah_soal': count})
        except Exception as e:
            return Response({'detail': f'Gagal membaca file Excel: {str(e)}'}, status=400)


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
        sesi_map = {s.ujian_id: (s.status, s.id) for s in SesiUjian.objects.filter(mahasiswa=request.user)}
        result = []
        for u in ujian_list:
            sesi_info = sesi_map.get(u.id, (None, None))
            result.append({
                'id': u.id,
                'judul': u.judul,
                'mata_pelajaran': u.mata_pelajaran.nama,
                'durasi_menit': u.durasi_menit,
                'jumlah_soal': u.jumlah_soal,
                'nilai_maksimal': u.nilai_maksimal,
                'tanggal_ujian': u.tanggal_ujian,
                'status_sesi': sesi_info[0],
                'sesi_id': sesi_info[1],
            })
        return Response(result)
