# Automatic Essay Scoring - Backend API

Sistem Backend REST API berbasis **Django** & **Django REST Framework (DRF)** yang dirancang untuk melakukan penilaian esai otomatis menggunakan kecerdasan buatan (**Ollama LLM - Llama 3.2:3b**) secara lokal. Sistem ini dilengkapi dengan modul **Zero Tolerance Proctoring** untuk mendeteksi kecurangan saat ujian berlangsung.

---

## Multi-Service Architecture

Proyek ini dibangun menggunakan arsitektur microservices terisolasi melalui **Docker Compose**:

1.  **`web`**: Django DRF Application server (berjalan di port `8000` internal, di-expose ke port **`8443`** host).
2.  **`db`**: PostgreSQL 15 sebagai database relasional utama.
3.  **`redis`**: Message broker untuk mendistribusikan antrean grading.
4.  **`celery`**: Worker asinkron yang memproses penilaian esai via LLM secara background.
5.  **`ollama`**: Server AI lokal tempat model LLM `llama3.2:3b` dieksekusi.

---

## Fitur Utama Backend

*   *** Auth & User Management**:
    *   Menggunakan **JWT Authentication** (`djangorestframework-simplejwt`).
    *   Login fleksibel: Bisa menggunakan **Username**, **NIM** (Mahasiswa), atau **NIP** (Dosen).
    *   **Single-Device Login Enforcement**: Mengunci sesi login hanya untuk satu perangkat aktif. Jika login di perangkat baru, token perangkat lama otomatis di-blacklist.
*   *** Zero-Tolerance Proctoring**:
    *   API Heartbeat berkala (setiap 15 detik) untuk mendeteksi status keaktifan mahasiswa.
    *   Pencatatan log pelanggaran kecurangan: *Membuka Tab Baru*, *Window Blur (Pindah Aplikasi)*, dan *Keluar Layar Fullscreen*.
    *   **Auto-Lock Akun**: Jika ada pelanggaran, ujian langsung dihentikan dan akun mahasiswa otomatis terkunci (`is_exam_locked=True`).
*   *** AI Automatic Grading**:
    *   Integrasi Celery worker ke Ollama secara lokal.
    *   Melakukan kalkulasi nilai esai (Skala 0, 5, 10) dengan pencocokan kata kunci dan referensi jawaban.
    *   Menyediakan feedback/alasan penilaian dalam Bahasa Indonesia secara otomatis.
*   *** Reporting & Export**:
    *   Export rekap nilai kelas berupa spreadsheet Excel (`.xlsx`) dengan styling tabel kustom.
    *   Export hasil ujian individu mahasiswa berupa dokumen PDF (`.pdf`) lengkap dengan detail penilaian per nomor soal.
*   *** Admin Customization**:
    *   Akses Django Admin eksklusif dibatasi hanya untuk **Superuser** (Administrator IT).
    *   Dynamic admin fields: Field NIM/NIP/Kelas otomatis bersembunyi secara dinamis (menggunakan vanilla JS) tergantung role user yang dipilih.

---

## Environment Variables (`.env`)

Buat file `.env` di direktori utama proyek (sudah diabaikan oleh `.gitignore` agar aman):

```env
DB_NAME=essay_db
DB_USER=essay_user
DB_PASSWORD=essay_password_2024
SECRET_KEY=-dsyr&i0j71@25_ffscbo1y4y#fl$@1^(v93c--n)9h5y&bi+b
DEBUG=1
REDIS_URL=redis://redis:6379/0
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b
```

---

## Panduan Instalasi & Run (Docker)

Pastikan **Docker Desktop** sudah berjalan di komputer Anda sebelum memulai.

### 1. Bangun & Jalankan Container
```bash
docker compose down -v  # Bersihkan cache volume lama jika ada conflict
docker compose up --build -d
```

### 2. Jalankan Migrasi Database
```bash
docker compose exec web python manage.py migrate
```

### 3. Buat Akun Superuser/Dosen Utama
```bash
docker compose exec web python manage.py createsuperuser
```
> Masukkan username yang tidak mengandung spasi (misalnya: `admin.dosen` atau `mustainul.abdi`).

### 4. Pull Model LLM (Hanya Sekali)
Unduh model Llama 3.2 ke dalam service Ollama Anda:
```bash
docker compose exec ollama ollama pull llama3.2:3b
```

### 5. Salin Static Files (Untuk Django Admin)
```bash
docker compose exec web python manage.py collectstatic --noinput
```

Sistem backend kini dapat diakses di: **`http://localhost:8443/api/v1/`** atau menggunakan IP LAN Anda (contoh: **`http://192.168.110.47:8443/api/v1/`**).

---

## Endpoint API Utama

### Authentication (`/api/v1/auth/`)
*   `POST /login/` : Login pengguna (dapat JWT Access & Refresh Token).
*   `POST /logout/` : Logout pengguna (memasukkan refresh token ke blacklist).
*   `GET /profile/` : Mengambil data diri profile pengguna yang aktif.
*   `GET /mahasiswa/` : (Dosen Only) Mengambil seluruh daftar mahasiswa.
*   `POST /mahasiswa/import/` : (Dosen Only) Upload data mahasiswa via Excel (.xlsx).
*   `GET /mahasiswa/export-kartu/` : (Dosen Only) Download PDF kartu login mahasiswa.
*   `POST /mahasiswa/<pk>/unlock/` : (Dosen Only) Membuka kembali akun mahasiswa yang terkunci karena pelanggaran.

### Ujian & Mata Kuliah (`/api/v1/ujian/`)
*   `GET | POST /mata-kuliah/` : Kelola daftar mata kuliah aktif.
*   `GET | POST /` : Kelola daftar ujian.
*   `POST /<pk>/aktivasi/` : Mengubah status ujian.
*   `GET /<pk>/monitor/` : Live monitor progress dan status pelanggaran peserta ujian.
*   `GET /tersedia/` : (Mahasiswa Only) Menampilkan ujian aktif yang siap dikerjakan berdasarkan kelas mahasiswa.

### Ujian & Submissions (`/api/v1/submission/`)
*   `POST /mulai/<ujian_pk>/` : Memulai sesi ujian baru atau melanjutkan sesi sebelumnya.
*   `POST /save-jawaban/` : Auto-save jawaban per nomor soal secara periodik.
*   `POST /submit/<sesi_pk>/` : Mengakhiri ujian dan mentrigger AI automatic grading di background.
*   `GET /hasil/<sesi_pk>/` : Memantau (polling) hasil kelulusan / nilai yang dinilai oleh AI.

### Proctoring/Pengawasan (`/api/v1/proctoring/`)
*   `POST /heartbeat/` : Mengirimkan signal keaktifan browser setiap 15 detik (mengembalikan sisa waktu ujian).
*   `POST /pelanggaran/` : Mencatat pelanggaran kecurangan (window blur / new tab / exit fullscreen) sekaligus langsung mengunci akun siswa.

### Laporan Nilai (`/api/v1/laporan/`)
*   `GET /nilai/<ujian_pk>/` : Ringkasan tabel nilai seluruh siswa kelas.
*   `GET /export/excel/<ujian_pk>/?kelas=<nama_kelas>` : Download berkas Excel styled nilai ujian mahasiswa.
*   `GET /export/pdf/<sesi_pk>/` : Download transkrip penilaian PDF individu mahasiswa (isi teks jawaban, skor, dan alasan penilaian dari AI).
