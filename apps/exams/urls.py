from django.urls import path
from .views import (
    DashboardDosenView,
    MataPelajaranListCreateView, MataPelajaranDetailView,
    UjianListCreateView, UjianDetailView, AktivasiUjianView, MonitorUjianView,
    SoalListCreateView, SoalDetailView, UploadSoalExcelView,
    UjianTersediaView,
)

app_name = 'exams'

urlpatterns = [
    # Dashboard dosen
    path('dashboard/', DashboardDosenView.as_view(), name='dashboard'),

    # Ujian tersedia untuk mahasiswa
    path('tersedia/', UjianTersediaView.as_view(), name='ujian_tersedia'),

    # Mata Kuliah
    path('mata-kuliah/', MataPelajaranListCreateView.as_view(), name='mata_kuliah_list'),
    path('mata-kuliah/<int:pk>/', MataPelajaranDetailView.as_view(), name='mata_kuliah_detail'),

    # Ujian
    path('', UjianListCreateView.as_view(), name='ujian_list'),
    path('<int:pk>/', UjianDetailView.as_view(), name='ujian_detail'),
    path('<int:pk>/aktivasi/', AktivasiUjianView.as_view(), name='aktivasi_ujian'),
    path('<int:pk>/monitor/', MonitorUjianView.as_view(), name='monitor_ujian'),

    # Soal
    path('<int:ujian_pk>/soal/', SoalListCreateView.as_view(), name='soal_list'),
    path('<int:ujian_pk>/soal/upload/', UploadSoalExcelView.as_view(), name='upload_soal'),
    path('soal/<int:pk>/', SoalDetailView.as_view(), name='soal_detail'),
]
