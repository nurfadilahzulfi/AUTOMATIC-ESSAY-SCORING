import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.grading.tasks import USER_PROMPT_TEMPLATE, _call_ollama

soal = "Jelaskan perbedaan antara Supervised Learning dan Unsupervised Learning beserta contoh algoritmanya masing-masing!"
referensi = "Supervised Learning menggunakan data berlabel (labeled data) di mana model dilatih memetakan input ke target output. Contoh: Linear Regression, Decision Tree, SVM. Unsupervised Learning menggunakan data tidak berlabel (unlabeled data) untuk menemukan pola alami atau pengelompokan data. Contoh: K-Means Clustering, PCA."
kata_kunci = "supervised, unsupervised, data berlabel, data tidak berlabel, linear regression, k-means"

# Jawaban mahasiswa menggunakan istilah ilmiah berbeda & algoritma berbeda yang TETAP BENAR
jawaban_mahasiswa_alternatif = (
    "Supervised learning adalah metode machine learning di mana model dilatih menggunakan data pasangan "
    "fitur dan target yang memiliki ground truth, contohnya Random Forest, Naive Bayes, dan Logistic Regression. "
    "Sedangkan Unsupervised learning mengeksplorasi struktur tersembunyi atau distribusi data tanpa adanya "
    "target label sebelumnya, contohnya DBSCAN, Hierarchical Clustering, dan t-SNE."
)

prompt = USER_PROMPT_TEMPLATE.format(
    pertanyaan=soal,
    referensi_jawaban=referensi,
    kata_kunci=kata_kunci,
    teks_jawaban=jawaban_mahasiswa_alternatif
)

print("Testing jawaban teori benar dengan kata kunci/contoh alternatif...")
result = _call_ollama(prompt)
print("Hasil penilaian AI:")
print(result)
