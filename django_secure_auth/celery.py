import os
from celery import Celery


# create your celery app hare

# settings.py ar location ta kothai setar path dite hobe r ha root file thekei celery run korte hobe
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_secure_auth.settings')


app = Celery("django_secure_auth")

# akhene settings.py ar moddhe celery ar config gula ki name thakebe , jemon celery_abc = true , akhon cei dict ba variable ar namer surute celery ase setai celery ar config dhore nibe
app.config_from_object('django.conf:settings', namespace='CELERY') 

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

