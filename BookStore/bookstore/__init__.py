from .celery import app as celery_app

#Init celery.
__all__ = ('celery_app',)