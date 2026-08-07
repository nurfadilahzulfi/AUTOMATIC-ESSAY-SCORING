from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

def _superuser_only(self, request):
    return request.user.is_active and request.user.is_superuser

admin.site.__class__.has_permission = _superuser_only

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('apps.accounts.urls', namespace='accounts')),
    path('api/v1/ujian/', include('apps.exams.urls', namespace='exams')),
    path('api/v1/submission/', include('apps.submissions.urls', namespace='submissions')),
    path('api/v1/proctoring/', include('apps.proctoring.urls', namespace='proctoring')),
    path('api/v1/laporan/', include('apps.reports.urls', namespace='reports')),

    # JWT token refresh (generic endpoint)
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
