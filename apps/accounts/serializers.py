from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserPublicSerializer(serializers.ModelSerializer):
    """Serializer publik — hanya data yang aman untuk dikembalikan ke frontend."""
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'nama_lengkap', 'nim', 'nip', 'kelas', 'role',
                  'role_display', 'is_exam_locked', 'lock_reason']
        read_only_fields = ['id', 'role_display', 'is_exam_locked', 'lock_reason']


class LoginSerializer(serializers.Serializer):
    """Serializer untuk login — menerima username/NIM + password."""
    username = serializers.CharField(help_text="Username atau NIM mahasiswa")
    password = serializers.CharField(write_only=True)


class ImportMahasiswaSerializer(serializers.Serializer):
    """Serializer untuk upload file Excel mahasiswa."""
    file_excel = serializers.FileField()


class DosenListSerializer(serializers.ModelSerializer):
    """Serializer khusus untuk menampilkan data dosen."""
    class Meta:
        model = User
        fields = ['id', 'username', 'nama_lengkap', 'nip', 'is_active', 'date_joined']
        read_only_fields = fields


class MahasiswaListSerializer(serializers.ModelSerializer):
    """Serializer khusus untuk menampilkan data mahasiswa."""
    class Meta:
        model = User
        fields = ['id', 'nama_lengkap', 'nim', 'kelas', 'is_exam_locked', 'lock_reason',
                  'locked_at', 'plain_password', 'date_joined']
        read_only_fields = fields
