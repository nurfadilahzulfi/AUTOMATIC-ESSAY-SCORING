from django.db import models
from django.conf import settings
from apps.exams.models import Ujian, Soal


class SesiUjian(models.Model):
    """
    Merepresentasikan satu sesi ujian mahasiswa.
    Satu mahasiswa hanya boleh punya satu sesi per ujian.
    """
    STATUS_BERLANGSUNG = 'berlangsung'
    STATUS_SELESAI = 'selesai'
    STATUS_PELANGGARAN = 'pelanggaran'
    STATUS_CHOICES = [
        (STATUS_BERLANGSUNG, 'Berlangsung'),
        (STATUS_SELESAI, 'Selesai'),
        (STATUS_PELANGGARAN, 'Dihentikan (Pelanggaran)'),
    ]

    mahasiswa = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sesi_ujian',
        verbose_name='Mahasiswa',
    )
    ujian = models.ForeignKey(
        Ujian,
        on_delete=models.CASCADE,
        related_name='sesi',
        verbose_name='Ujian',
    )
    waktu_mulai = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Mulai')
    waktu_selesai = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Selesai')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_BERLANGSUNG,
        verbose_name='Status Sesi',
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Address')
    total_nilai = models.IntegerField(null=True, blank=True, verbose_name='Total Nilai')
    last_heartbeat = models.DateTimeField(null=True, blank=True, verbose_name='Heartbeat Terakhir')

    class Meta:
        verbose_name = 'Sesi Ujian'
        verbose_name_plural = 'Daftar Sesi Ujian'
        ordering = ['-waktu_mulai']
        # Satu mahasiswa hanya boleh punya satu sesi per ujian
        unique_together = ['mahasiswa', 'ujian']

    def __str__(self):
        return f"{self.mahasiswa.nama_lengkap} — {self.ujian.judul} ({self.status})"

    @property
    def durasi_berlangsung(self):
        """Menghitung durasi ujian dalam menit."""
        if self.waktu_selesai:
            delta = self.waktu_selesai - self.waktu_mulai
        else:
            from django.utils import timezone
            delta = timezone.now() - self.waktu_mulai
        return int(delta.total_seconds() / 60)

    @property
    def semua_selesai_dinilai(self):
        return self.jawaban.filter(grading_status='done').count() == self.ujian.jumlah_soal


class Jawaban(models.Model):
    """Satu jawaban esai mahasiswa untuk satu soal."""
    GRADING_PENDING = 'pending'
    GRADING_PROCESSING = 'processing'
    GRADING_DONE = 'done'
    GRADING_FAILED = 'failed'
    GRADING_STATUS_CHOICES = [
        (GRADING_PENDING, 'Menunggu Penilaian'),
        (GRADING_PROCESSING, 'Sedang Dinilai'),
        (GRADING_DONE, 'Selesai Dinilai'),
        (GRADING_FAILED, 'Gagal Dinilai'),
    ]

    NILAI_CHOICES = [
        (0, '0 — Tidak Relevan'),
        (5, '5 — Sebagian Benar'),
        (10, '10 — Lengkap dan Tepat'),
    ]

    sesi = models.ForeignKey(
        SesiUjian,
        on_delete=models.CASCADE,
        related_name='jawaban',
        verbose_name='Sesi Ujian',
    )
    soal = models.ForeignKey(
        Soal,
        on_delete=models.CASCADE,
        related_name='jawaban',
        verbose_name='Soal',
    )
    teks_jawaban = models.TextField(verbose_name='Teks Jawaban', blank=True)
    nilai = models.IntegerField(
        null=True,
        blank=True,
        choices=NILAI_CHOICES,
        verbose_name='Nilai',
    )
    alasan_nilai = models.TextField(
        blank=True,
        verbose_name='Alasan Penilaian AI',
    )
    grading_status = models.CharField(
        max_length=20,
        choices=GRADING_STATUS_CHOICES,
        default=GRADING_PENDING,
        verbose_name='Status Penilaian',
    )
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Submit')
    graded_at = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Dinilai')

    class Meta:
        verbose_name = 'Jawaban'
        verbose_name_plural = 'Daftar Jawaban'
        ordering = ['soal__nomor_urut']
        unique_together = ['sesi', 'soal']

    def __str__(self):
        return f"Jawaban Soal {self.soal.nomor_urut} — {self.sesi.mahasiswa.nama_lengkap}"
