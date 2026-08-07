import random
import string
import io

from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from .models import User
from .serializers import UserPublicSerializer, MahasiswaListSerializer, DosenListSerializer


def _generate_password(length=6):
    chars = string.digits + string.ascii_uppercase
    return ''.join(random.choices(chars, k=length))



class LoginView(APIView):
    """
    POST /api/v1/auth/login/
    Login dengan username/NIM + password.
    Mengembalikan JWT access & refresh token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        if not username or not password:
            return Response({'detail': 'Username dan password wajib diisi.'}, status=400)

        # Coba authenticate langsung
        user = authenticate(request, username=username, password=password)

        # Jika gagal, coba cari berdasarkan NIM (mahasiswa)
        if user is None:
            try:
                u = User.objects.get(nim=username, role=User.ROLE_MAHASISWA)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                pass

        # Jika masih gagal, coba cari berdasarkan NIP (dosen)
        if user is None:
            try:
                u = User.objects.get(nip=username, role=User.ROLE_DOSEN)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None:
            return Response({'detail': 'NIM/Username atau password salah.'}, status=401)

        if user.is_exam_locked:
            return Response({
                'detail': 'Akun Anda dikunci karena pelanggaran ujian.',
                'lock_reason': user.lock_reason,
            }, status=403)

        if not user.is_active:
            return Response({'detail': 'Akun tidak aktif.'}, status=403)

        # ── SINGLE-DEVICE ENFORCEMENT ──────────────────────────────────────
        # Blacklist semua refresh token lama milik user ini.
        # Perangkat lain yang sedang login akan otomatis ter-logout
        # saat access token mereka expired (maks 4 jam).
        try:
            from rest_framework_simplejwt.token_blacklist.models import (
                OutstandingToken, BlacklistedToken
            )
            outstanding_tokens = OutstandingToken.objects.filter(user=user)
            for token in outstanding_tokens:
                BlacklistedToken.objects.get_or_create(token=token)
        except Exception:
            pass  

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserPublicSerializer(user).data,
        })


class LogoutView(APIView):
    """POST /api/v1/auth/logout/ — Blacklist refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Berhasil logout.'})
        except Exception:
            return Response({'detail': 'Token tidak valid.'}, status=400)


class ProfileView(APIView):
    """GET /api/v1/auth/profile/ — Profil user yang sedang login."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserPublicSerializer(request.user).data)



class MahasiswaListView(APIView):
    """GET /api/v1/auth/mahasiswa/ — Daftar semua mahasiswa."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_dosen:
            return Response({'detail': 'Akses ditolak.'}, status=403)
        kelas = request.query_params.get('kelas', '')
        qs = User.objects.filter(role=User.ROLE_MAHASISWA).order_by('kelas', 'nama_lengkap')
        if kelas:
            qs = qs.filter(kelas=kelas)
        return Response(MahasiswaListSerializer(qs, many=True).data)


class ImportMahasiswaView(APIView):
    """
    POST /api/v1/auth/mahasiswa/import/
    Upload file Excel berisi data mahasiswa (nama, nim, kelas).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_dosen:
            return Response({'detail': 'Akses ditolak.'}, status=403)

        excel_file = request.FILES.get('file_excel')
        if not excel_file:
            return Response({'detail': 'File Excel wajib dilampirkan.'}, status=400)

        try:
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            berhasil, gagal, duplikat = 0, 0, []

            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row[0]:
                    continue
                nama = str(row[0]).strip()
                nim = str(row[1]).strip()
                kelas = str(row[2]).strip() if len(row) > 2 and row[2] else ''

                if User.objects.filter(nim=nim).exists():
                    duplikat.append(nim)
                    gagal += 1
                    continue

                password = _generate_password()
                User.objects.create_user(
                    username=nim,
                    password=password,
                    nama_lengkap=nama,
                    nim=nim,
                    kelas=kelas,
                    role=User.ROLE_MAHASISWA,
                    plain_password=password,
                )
                berhasil += 1

            return Response({
                'detail': f'Berhasil mengimpor {berhasil} mahasiswa.',
                'berhasil': berhasil,
                'gagal': gagal,
                'nim_duplikat': duplikat,
            })
        except Exception as e:
            return Response({'detail': f'Gagal membaca file Excel: {str(e)}'}, status=400)


class ExportKartuUjianView(APIView):
    """
    GET /api/v1/auth/mahasiswa/export-kartu/?kelas=TI-3A
    Export daftar username+password ke PDF.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_dosen:
            return Response({'detail': 'Akses ditolak.'}, status=403)

        kelas_filter = request.query_params.get('kelas', '')
        qs = User.objects.filter(role=User.ROLE_MAHASISWA).order_by('kelas', 'nama_lengkap')
        if kelas_filter:
            qs = qs.filter(kelas=kelas_filter)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        elements = []

        title_style = ParagraphStyle('title', parent=styles['Heading1'], alignment=1, spaceAfter=20)
        elements.append(Paragraph("Kartu Ujian Mahasiswa", title_style))
        if kelas_filter:
            elements.append(Paragraph(f"Kelas: {kelas_filter}", styles['Normal']))
        elements.append(Spacer(1, 0.5*cm))

        data = [['No', 'Nama Lengkap', 'NIM (Username)', 'Kelas', 'Password']]
        for i, mhs in enumerate(qs, 1):
            data.append([str(i), mhs.nama_lengkap, mhs.nim, mhs.kelas, mhs.plain_password or '—'])

        table = Table(data, colWidths=[1*cm, 6*cm, 4*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')]),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)

        fname = f"kartu_ujian_{kelas_filter or 'semua'}.pdf"
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{fname}"'
        return response


class UnlockMahasiswaView(APIView):
    """POST /api/v1/auth/mahasiswa/<pk>/unlock/ — Buka kunci akun mahasiswa."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_dosen:
            return Response({'detail': 'Akses ditolak.'}, status=403)
        try:
            mhs = User.objects.get(pk=pk, role=User.ROLE_MAHASISWA)
        except User.DoesNotExist:
            return Response({'detail': 'Mahasiswa tidak ditemukan.'}, status=404)

        mhs.is_exam_locked = False
        mhs.lock_reason = ''
        mhs.locked_at = None
        mhs.save()
        return Response({'detail': f'Akun {mhs.nama_lengkap} berhasil dibuka kuncinya.'})


class HapusMahasiswaView(APIView):
    """DELETE /api/v1/auth/mahasiswa/<pk>/ — Hapus akun mahasiswa."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not request.user.is_dosen:
            return Response({'detail': 'Akses ditolak.'}, status=403)
        try:
            mhs = User.objects.get(pk=pk, role=User.ROLE_MAHASISWA)
        except User.DoesNotExist:
            return Response({'detail': 'Mahasiswa tidak ditemukan.'}, status=404)
        nama = mhs.nama_lengkap
        mhs.delete()
        return Response({'detail': f'Data mahasiswa {nama} berhasil dihapus.'})
