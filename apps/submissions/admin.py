from django.contrib import admin
from .models import SesiUjian, Jawaban


class JawabanInline(admin.TabularInline):
    model = Jawaban
    extra = 0
    readonly_fields = ['soal', 'teks_jawaban', 'nilai', 'alasan_nilai', 'grading_status', 'graded_at']
    can_delete = False


@admin.register(SesiUjian)
class SesiUjianAdmin(admin.ModelAdmin):
    list_display = ['mahasiswa', 'ujian', 'status', 'total_nilai', 'waktu_mulai', 'waktu_selesai']
    list_filter = ['status', 'ujian']
    search_fields = ['mahasiswa__nama_lengkap', 'mahasiswa__nim']
    readonly_fields = ['waktu_mulai', 'ip_address', 'last_heartbeat']
    inlines = [JawabanInline]
    actions = ['regrade_sesi']

    @admin.action(description='Nilai Ulang Sesi Ujian (AI)')
    def regrade_sesi(self, request, queryset):
        from apps.grading.tasks import grade_sesi_task
        for sesi in queryset:
            # Reset status grading semua jawaban pada sesi ini ke pending
            for jawaban in sesi.jawaban.all():
                jawaban.grading_status = Jawaban.GRADING_PENDING
                jawaban.nilai = None
                jawaban.alasan_nilai = ''
                jawaban.save()
            sesi.total_nilai = None
            sesi.save()
            # Jalankan task Celery
            grade_sesi_task.delay(sesi.pk)
        self.message_user(request, f"Penilaian ulang menggunakan AI berhasil dipicu untuk {queryset.count()} sesi ujian.")


@admin.register(Jawaban)
class JawabanAdmin(admin.ModelAdmin):
    list_display = ['sesi', 'soal', 'nilai', 'grading_status', 'graded_at']
    list_filter = ['grading_status', 'nilai']
    readonly_fields = ['submitted_at', 'graded_at']
    actions = ['regrade_jawaban']

    @admin.action(description='Nilai Ulang Jawaban Terpilih (AI)')
    def regrade_jawaban(self, request, queryset):
        from apps.grading.tasks import grade_jawaban_task
        for jawaban in queryset:
            jawaban.grading_status = Jawaban.GRADING_PENDING
            jawaban.nilai = None
            jawaban.alasan_nilai = ''
            jawaban.save()
            
            # Reset juga total_nilai di SesiUjian agar dihitung ulang
            sesi = jawaban.sesi
            sesi.total_nilai = None
            sesi.save()
            
            # Jalankan task Celery
            grade_jawaban_task.delay(jawaban.pk)
        self.message_user(request, f"Penilaian ulang menggunakan AI berhasil dipicu untuk {queryset.count()} jawaban.")

