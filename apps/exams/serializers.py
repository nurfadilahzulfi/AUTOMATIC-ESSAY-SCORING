from rest_framework import serializers
from .models import MataPelajaran, Ujian, Soal


class MataPelajaranSerializer(serializers.ModelSerializer):
    dosen_nama = serializers.CharField(source='dosen.nama_lengkap', read_only=True)

    class Meta:
        model = MataPelajaran
        fields = ['id', 'nama', 'kode', 'dosen', 'dosen_nama', 'created_at']
        read_only_fields = ['id', 'dosen', 'dosen_nama', 'created_at']


class SoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soal
        fields = ['id', 'nomor_urut', 'pertanyaan', 'referensi_jawaban', 'kata_kunci']


class SoalPublicSerializer(serializers.ModelSerializer):
    """Serializer soal untuk mahasiswa — tanpa referensi jawaban."""
    class Meta:
        model = Soal
        fields = ['id', 'nomor_urut', 'pertanyaan']


class UjianSerializer(serializers.ModelSerializer):
    mata_kuliah_nama = serializers.CharField(source='mata_pelajaran.nama', read_only=True)
    mata_kuliah_kode = serializers.CharField(source='mata_pelajaran.kode', read_only=True)
    jumlah_soal = serializers.IntegerField(read_only=True)
    nilai_maksimal = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Ujian
        fields = ['id', 'judul', 'deskripsi', 'mata_pelajaran', 'mata_kuliah_nama',
                  'mata_kuliah_kode', 'durasi_menit', 'kelas_target', 'status',
                  'status_display', 'jumlah_soal', 'nilai_maksimal', 'tanggal_ujian',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'jumlah_soal', 'nilai_maksimal', 'created_at', 'updated_at']


class UjianDetailSerializer(UjianSerializer):
    """Detail ujian beserta daftar soal (untuk dosen)."""
    soal = SoalSerializer(many=True, read_only=True)

    class Meta(UjianSerializer.Meta):
        fields = UjianSerializer.Meta.fields + ['soal']


class UjianMahasiswaSerializer(serializers.ModelSerializer):
    """Ujian untuk mahasiswa — soal tanpa referensi jawaban."""
    soal = SoalPublicSerializer(many=True, read_only=True)
    mata_kuliah_nama = serializers.CharField(source='mata_pelajaran.nama', read_only=True)
    jumlah_soal = serializers.IntegerField(read_only=True)
    nilai_maksimal = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ujian
        fields = ['id', 'judul', 'deskripsi', 'mata_kuliah_nama', 'durasi_menit',
                  'jumlah_soal', 'nilai_maksimal', 'tanggal_ujian', 'soal']
