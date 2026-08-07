"""
apps/reports/admin.py

App reports tidak mendaftarkan model baru ke admin karena:
- SesiUjian & Jawaban sudah dikelola di apps/submissions/admin.py
- PelanggaranLog sudah dikelola di apps/proctoring/admin.py

Laporan dan export data diakses melalui REST API:
  GET /api/v1/laporan/nilai/<ujian_pk>/
  GET /api/v1/laporan/export/excel/<ujian_pk>/
  GET /api/v1/laporan/export/pdf/<sesi_pk>/
"""
from django.contrib import admin  # noqa: F401
