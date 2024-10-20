import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# celery теперь знает где лежат наши конфигурации по ключевому слову (namespace='CELERY')
# например CELERY_RESULT_BACKEND
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_connection_retry_on_startup = True

# строчка нужна для автообнаружения задач в различный приложениях
# например мы создали файл tasks в приложении dogs и задачи, помеченные декоратором будут обнаружены.
app.autodiscover_tasks()
