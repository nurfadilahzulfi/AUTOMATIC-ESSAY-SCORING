from django.urls import path
from .views import (
    LoginView, LogoutView, ProfileView,
    MahasiswaListView, ImportMahasiswaView, ExportKartuUjianView,
    UnlockMahasiswaView, HapusMahasiswaView,
)

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Manajemen mahasiswa (dosen only)
    path('mahasiswa/', MahasiswaListView.as_view(), name='daftar_mahasiswa'),
    path('mahasiswa/import/', ImportMahasiswaView.as_view(), name='import_mahasiswa'),
    path('mahasiswa/export-kartu/', ExportKartuUjianView.as_view(), name='export_kartu_ujian'),
    path('mahasiswa/<int:pk>/unlock/', UnlockMahasiswaView.as_view(), name='unlock_mahasiswa'),
    path('mahasiswa/<int:pk>/', HapusMahasiswaView.as_view(), name='hapus_mahasiswa'),
]
