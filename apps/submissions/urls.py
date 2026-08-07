from django.urls import path
from .views import (
    MulaiUjianView, SesiUjianDetailView,
    SaveJawabanView, SubmitUjianView, HasilUjianView,
)

app_name = 'submissions'

urlpatterns = [
    path('mulai/<int:ujian_pk>/', MulaiUjianView.as_view(), name='mulai_ujian'),
    path('sesi/<int:sesi_pk>/', SesiUjianDetailView.as_view(), name='sesi_detail'),
    path('save-jawaban/', SaveJawabanView.as_view(), name='save_jawaban'),
    path('submit/<int:sesi_pk>/', SubmitUjianView.as_view(), name='submit_ujian'),
    path('hasil/<int:sesi_pk>/', HasilUjianView.as_view(), name='hasil_ujian'),
]
