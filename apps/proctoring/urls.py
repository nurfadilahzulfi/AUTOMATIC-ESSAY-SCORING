from django.urls import path
from .views import HeartbeatView, CatatPelanggaranView

app_name = 'proctoring'

urlpatterns = [
    path('heartbeat/', HeartbeatView.as_view(), name='heartbeat'),
    path('pelanggaran/', CatatPelanggaranView.as_view(), name='catat_pelanggaran'),
]
