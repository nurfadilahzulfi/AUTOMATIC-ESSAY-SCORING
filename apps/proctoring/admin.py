from django.contrib import admin
from .models import HeartbeatLog, PelanggaranLog


@admin.register(HeartbeatLog)
class HeartbeatLogAdmin(admin.ModelAdmin):
    list_display = ['sesi', 'timestamp']
    list_filter = ['sesi__ujian']
    search_fields = ['sesi__mahasiswa__nama_lengkap', 'sesi__mahasiswa__nim']
    readonly_fields = ['sesi', 'timestamp']

    def has_add_permission(self, request):
        return False  # Log tidak boleh dibuat manual


@admin.register(PelanggaranLog)
class PelanggaranLogAdmin(admin.ModelAdmin):
    list_display = ['get_mahasiswa', 'get_ujian', 'tipe', 'timestamp', 'keterangan']
    list_filter = ['tipe', 'sesi__ujian']
    search_fields = ['sesi__mahasiswa__nama_lengkap', 'sesi__mahasiswa__nim']
    readonly_fields = ['sesi', 'tipe', 'timestamp', 'keterangan', 'user_agent']

    def has_add_permission(self, request):
        return False  # Log tidak boleh dibuat manual

    @admin.display(description='Mahasiswa')
    def get_mahasiswa(self, obj):
        return obj.sesi.mahasiswa.nama_lengkap

    @admin.display(description='Ujian')
    def get_ujian(self, obj):
        return obj.sesi.ujian.judul
