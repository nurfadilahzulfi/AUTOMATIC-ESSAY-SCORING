from django.apps import AppConfig


class GradingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.grading'
    verbose_name = 'Penilaian AI'

    def ready(self):
        # Pastikan Celery task terdaftar saat aplikasi siap
        import apps.grading.tasks  # noqa: F401
