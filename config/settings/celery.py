from config.env import env

# config
CELERY_TIMEZONE = "UTC"
CELERY_TASK_SOFT_TIME_LIMIT = 20
CELERY_TASK_TIME_LIMIT = 30
CELERY_TASK_MAX_RETRIES = 3
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", "")
CELERY_RESULT_EXTENDED = True
CELERY_EMAIL_TASK_CONFIG = {
    "name": "djcelery_email_send",
    "ignore_result": False,
}
