# monitoring_printers/celery.py
import os
from celery import Celery

# Устанавливаем переменную окружения с настройками Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring_printers.settings')

# Создаем экземпляр приложения Celery
app = Celery('monitoring_printers')

# Загружаем настройки из settings.py (с префиксом CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях Django
app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')