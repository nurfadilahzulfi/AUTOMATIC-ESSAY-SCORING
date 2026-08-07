from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'nama_lengkap', 'get_nomor_id', 'kelas', 'role', 'is_exam_locked', 'is_active']
    list_filter = ['role', 'kelas', 'is_exam_locked', 'is_active']
    search_fields = ['username', 'nama_lengkap', 'nim', 'nip']
    ordering = ['role', 'kelas', 'nama_lengkap']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informasi Akademik', {
            'fields': ('role', 'nama_lengkap', 'nip', 'nim', 'kelas', 'plain_password'),
        }),
        ('Status Ujian', {
            'fields': ('is_exam_locked', 'lock_reason', 'locked_at'),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informasi Akademik', {
            'fields': ('role', 'nama_lengkap', 'nip', 'nim', 'kelas'),
        }),
    )

    class Media:
        js = ('admin/js/nim_nip_toggle.js',)

    @admin.display(description='NIM / NIP')
    def get_nomor_id(self, obj):
        if obj.role == User.ROLE_DOSEN:
            return f"NIP: {obj.nip or '—'}"
        return f"NIM: {obj.nim or '—'}"
