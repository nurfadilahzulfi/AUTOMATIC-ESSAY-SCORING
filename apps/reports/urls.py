from django.urls import path
from .views import NilaiUjianView, LogPelanggaranView, ExportExcelView, ExportPDFMahasiswaView

app_name = 'reports'

urlpatterns = [
    path('nilai/<int:ujian_pk>/', NilaiUjianView.as_view(), name='nilai_ujian'),
    path('log-pelanggaran/<int:ujian_pk>/', LogPelanggaranView.as_view(), name='log_pelanggaran'),
    path('export/excel/<int:ujian_pk>/', ExportExcelView.as_view(), name='export_excel'),
    path('export/pdf/<int:sesi_pk>/', ExportPDFMahasiswaView.as_view(), name='export_pdf'),
]
