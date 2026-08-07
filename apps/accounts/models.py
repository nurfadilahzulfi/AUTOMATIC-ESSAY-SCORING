from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User Model untuk Dosen dan Mahasiswa.
    Field username digunakan sebagai identifier login.
    """
    ROLE_DOSEN = 'dosen'
    ROLE_MAHASISWA = 'mahasiswa'
    ROLE_CHOICES = [
        (ROLE_DOSEN, 'Dosen'),
        (ROLE_MAHASISWA, 'Mahasiswa'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MAHASISWA,
        verbose_name='Peran',
    )
    nama_lengkap = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nama Lengkap',
    )
    nim = models.CharField(
        max_length=50,
        blank=True,
        unique=False,  # Khusus mahasiswa
        verbose_name='NIM',
        help_text='Nomor Induk Mahasiswa. Diisi hanya untuk mahasiswa.',
    )
    nip = models.CharField(
        max_length=50,
        blank=True,
        unique=False,  # Khusus dosen
        verbose_name='NIP',
        help_text='Nomor Induk Pegawai. Diisi hanya untuk dosen.',
    )
    kelas = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Kelas',
    )

    # Penguncian akun karena pelanggaran ujian
    is_exam_locked = models.BooleanField(
        default=False,
        verbose_name='Akun Dikunci (Pelanggaran Ujian)',
    )
    lock_reason = models.TextField(
        blank=True,
        verbose_name='Alasan Penguncian',
    )
    locked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Waktu Dikunci',
    )

    # Password plaintext (hanya untuk ditampilkan saat generate, tidak disimpan permanen)
    plain_password = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Password (untuk dicetak)',
        help_text='Disimpan sementara untuk keperluan cetak kartu ujian.',
    )

    class Meta:
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Daftar Pengguna'
        ordering = ['kelas', 'nama_lengkap']

    def __str__(self):
        if self.role == self.ROLE_MAHASISWA:
            return f"{self.nama_lengkap} ({self.nim}) - {self.kelas}"
        return f"{self.nama_lengkap} - NIP: {self.nip or 'belum diisi'} (Dosen)"

    @property
    def is_dosen(self):
        return self.role == self.ROLE_DOSEN

    @property
    def is_mahasiswa(self):
        return self.role == self.ROLE_MAHASISWA

    def get_full_name(self):
        return self.nama_lengkap or self.username
