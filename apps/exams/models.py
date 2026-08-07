from django.db import models
from django.conf import settings


class MataPelajaran(models.Model):
    """Mata kuliah yang diajar oleh dosen."""
    nama = models.CharField(max_length=200, verbose_name='Nama Mata Kuliah')
    kode = models.CharField(max_length=20, unique=True, verbose_name='Kode Mata Kuliah')
    dosen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mata_kuliah',
        verbose_name='Dosen Pengampu',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mata Kuliah'
        verbose_name_plural = 'Daftar Mata Kuliah'
        ordering = ['nama']

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class Ujian(models.Model):
    """Satu sesi ujian esai untuk satu mata pelajaran dan kelas tertentu."""
    STATUS_DRAFT = 'draft'
    STATUS_AKTIF = 'aktif'
    STATUS_SELESAI = 'selesai'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_AKTIF, 'Aktif'),
        (STATUS_SELESAI, 'Selesai'),
    ]

    mata_pelajaran = models.ForeignKey(
        MataPelajaran,
        on_delete=models.CASCADE,
        related_name='ujian',
        verbose_name='Mata Pelajaran',
    )
    judul = models.CharField(max_length=300, verbose_name='Judul Ujian')
    deskripsi = models.TextField(blank=True, verbose_name='Deskripsi / Petunjuk Ujian')
    durasi_menit = models.PositiveIntegerField(default=90, verbose_name='Durasi (menit)')
    kelas_target = models.CharField(
        max_length=200,
        verbose_name='Kelas yang Diizinkan',
        help_text='Pisahkan dengan koma jika lebih dari satu kelas. Contoh: TI-3A, TI-3B',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name='Status Ujian',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tanggal_ujian = models.DateField(null=True, blank=True, verbose_name='Tanggal Ujian')

    class Meta:
        verbose_name = 'Ujian'
        verbose_name_plural = 'Daftar Ujian'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.judul} — {self.mata_pelajaran.kode}"

    def get_kelas_list(self):
        """Mengembalikan daftar kelas yang diizinkan."""
        return [k.strip() for k in self.kelas_target.split(',')]

    @property
    def jumlah_soal(self):
        return self.soal.count()

    @property
    def nilai_maksimal(self):
        """Nilai maksimal = jumlah soal × 10."""
        return self.jumlah_soal * 10


class Soal(models.Model):
    """Satu butir soal esai dalam sebuah ujian."""
    ujian = models.ForeignKey(
        Ujian,
        on_delete=models.CASCADE,
        related_name='soal',
        verbose_name='Ujian',
    )
    nomor_urut = models.PositiveIntegerField(verbose_name='Nomor Soal')
    pertanyaan = models.TextField(verbose_name='Pertanyaan')
    referensi_jawaban = models.TextField(
        verbose_name='Referensi Jawaban',
        help_text='Jawaban kunci/acuan yang digunakan AI sebagai panduan penilaian.',
    )
    kata_kunci = models.TextField(
        blank=True,
        verbose_name='Kata Kunci Penting',
        help_text='Pisahkan dengan koma. Contoh: enkapsulasi, inheritance, polimorfisme',
    )

    class Meta:
        verbose_name = 'Soal'
        verbose_name_plural = 'Daftar Soal'
        ordering = ['ujian', 'nomor_urut']
        unique_together = ['ujian', 'nomor_urut']

    def __str__(self):
        return f"Soal {self.nomor_urut} — {self.ujian.judul}"

    def get_kata_kunci_list(self):
        return [k.strip() for k in self.kata_kunci.split(',') if k.strip()]
