from django.urls import path
from .views import KelasListView
from .views import (
    LoginView, LogoutView, ProfileView,
    MahasiswaListView, ImportMahasiswaView, ExportKartuUjianView,
    UnlockMahasiswaView, HapusMahasiswaView,
    TambahMahasiswaSatuView, KelasRenameView,
)

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Manajemen mahasiswa (dosen only / authenticated)
    path('kelas/', KelasListView.as_view(), name='daftar_kelas_unik'), # <--- Tambahkan baris ini
    # Manajemen mahasiswa (dosen only)
    path('mahasiswa/', MahasiswaListView.as_view(), name='daftar_mahasiswa'),
    path('mahasiswa/import/', ImportMahasiswaView.as_view(), name='import_mahasiswa'),
    path('mahasiswa/tambah/', TambahMahasiswaSatuView.as_view(), name='tambah_mahasiswa_satu'),
    path('mahasiswa/export-kartu/', ExportKartuUjianView.as_view(), name='export_kartu_ujian'),
    path('mahasiswa/<int:pk>/unlock/', UnlockMahasiswaView.as_view(), name='unlock_mahasiswa'),
    path('mahasiswa/<int:pk>/', HapusMahasiswaView.as_view(), name='hapus_mahasiswa'),
    path('kelas/rename/', KelasRenameView.as_view(), name='kelas_rename'),
]
