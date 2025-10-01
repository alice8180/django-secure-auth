from decouple import config


# configure celery or rabbitmq hare


CELERY_BROKER_URL = config("CELERY_BROKER_URL")

# CELERY_RESULT_BACKEND = 'django-db'   # celery kono kon kajj ses korlo tar log db te save korte ata use kora hoy
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'



"""config auto inactive or unverified user delete"""
default_schedule = 3600
CELERY_BEAT_SCHEDULE = {
    "cleanup-unverified-users-every-hour": {
        "task": "celery_tasks.notifications.cleanup_unverified_users",
        "schedule": default_schedule,  # proti ghontai ekbar kore ai delete inactive user function celery te auto run hobe
    },
    "cleanup-invalid-token-every-hour": {
        "task": "celery_tasks.notifications.cleanup_invalid_verify_token", 
        "schedule": default_schedule,
    },
}
