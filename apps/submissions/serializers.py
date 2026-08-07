from rest_framework import serializers
from .models import SesiUjian, Jawaban


class JawabanSerializer(serializers.ModelSerializer):
    soal_nomor = serializers.IntegerField(source='soal.nomor_urut', read_only=True)
    soal_pertanyaan = serializers.CharField(source='soal.pertanyaan', read_only=True)
    grading_status_display = serializers.CharField(source='get_grading_status_display', read_only=True)
    nilai_display = serializers.CharField(source='get_nilai_display', read_only=True)

    class Meta:
        model = Jawaban
        fields = ['id', 'soal', 'soal_nomor', 'soal_pertanyaan', 'teks_jawaban',
                  'nilai', 'nilai_display', 'alasan_nilai', 'grading_status',
                  'grading_status_display', 'submitted_at', 'graded_at']
        read_only_fields = ['id', 'soal_nomor', 'soal_pertanyaan', 'nilai', 'nilai_display',
                            'alasan_nilai', 'grading_status', 'grading_status_display',
                            'submitted_at', 'graded_at']


class SaveJawabanSerializer(serializers.Serializer):
    """Untuk auto-save jawaban dari frontend."""
    soal_id = serializers.IntegerField()
    teks_jawaban = serializers.CharField(allow_blank=True, required=False, default='')


class SesiUjianSerializer(serializers.ModelSerializer):
    mahasiswa_nama = serializers.CharField(source='mahasiswa.nama_lengkap', read_only=True)
    mahasiswa_nim = serializers.CharField(source='mahasiswa.nim', read_only=True)
    mahasiswa_kelas = serializers.CharField(source='mahasiswa.kelas', read_only=True)
    ujian_judul = serializers.CharField(source='ujian.judul', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    jawaban = JawabanSerializer(many=True, read_only=True)
    nilai_maksimal = serializers.IntegerField(source='ujian.nilai_maksimal', read_only=True)

    class Meta:
        model = SesiUjian
        fields = ['id', 'mahasiswa', 'mahasiswa_nama', 'mahasiswa_nim', 'mahasiswa_kelas',
                  'ujian', 'ujian_judul', 'waktu_mulai', 'waktu_selesai', 'status',
                  'status_display', 'total_nilai', 'nilai_maksimal', 'jawaban']
        read_only_fields = fields


class SesiUjianListSerializer(serializers.ModelSerializer):
    """Versi ringkas untuk daftar peserta (tanpa detail jawaban)."""
    mahasiswa_nama = serializers.CharField(source='mahasiswa.nama_lengkap', read_only=True)
    mahasiswa_nim = serializers.CharField(source='mahasiswa.nim', read_only=True)
    mahasiswa_kelas = serializers.CharField(source='mahasiswa.kelas', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    nilai_maksimal = serializers.IntegerField(source='ujian.nilai_maksimal', read_only=True)

    class Meta:
        model = SesiUjian
        fields = ['id', 'mahasiswa_nama', 'mahasiswa_nim', 'mahasiswa_kelas',
                  'status', 'status_display', 'total_nilai', 'nilai_maksimal',
                  'waktu_mulai', 'waktu_selesai']
