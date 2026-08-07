from django.db import models
from apps.submissions.models import SesiUjian


class HeartbeatLog(models.Model):
    """Log detak jantung dari browser mahasiswa (setiap 15 detik)."""
    sesi = models.ForeignKey(
        SesiUjian,
        on_delete=models.CASCADE,
        related_name='heartbeats',
        verbose_name='Sesi Ujian',
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Waktu')

    class Meta:
        verbose_name = 'Log Heartbeat'
        verbose_name_plural = 'Log Heartbeat'
        ordering = ['-timestamp']
        # Hanya simpan yang terbaru, tidak perlu semua history
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"Heartbeat: {self.sesi.mahasiswa.nama_lengkap} @ {self.timestamp}"


class PelanggaranLog(models.Model):
    """Log setiap kejadian pelanggaran selama ujian."""
    TIPE_TAB_BARU = 'tab_baru'
    TIPE_WINDOW_BLUR = 'window_blur'
    TIPE_FULLSCREEN_EXIT = 'fullscreen_exit'
    TIPE_HEARTBEAT_TIMEOUT = 'heartbeat_timeout'
    TIPE_CHOICES = [
        (TIPE_TAB_BARU, 'Membuka Tab/Jendela Baru'),
        (TIPE_WINDOW_BLUR, 'Berpindah Aplikasi/Jendela'),
        (TIPE_FULLSCREEN_EXIT, 'Keluar dari Mode Layar Penuh'),
        (TIPE_HEARTBEAT_TIMEOUT, 'Koneksi Terputus (Heartbeat Timeout)'),
    ]

    sesi = models.ForeignKey(
        SesiUjian,
        on_delete=models.CASCADE,
        related_name='pelanggaran',
        verbose_name='Sesi Ujian',
    )
    tipe = models.CharField(
        max_length=30,
        choices=TIPE_CHOICES,
        verbose_name='Jenis Pelanggaran',
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Pelanggaran')
    keterangan = models.TextField(blank=True, verbose_name='Keterangan Tambahan')
    user_agent = models.TextField(blank=True, verbose_name='User Agent Browser')

    class Meta:
        verbose_name = 'Log Pelanggaran'
        verbose_name_plural = 'Log Pelanggaran'
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.get_tipe_display()}] {self.sesi.mahasiswa.nama_lengkap} @ {self.timestamp}"
