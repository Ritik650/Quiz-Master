from celery import Celery

def make_celery():
    celery = Celery(
        'quizmaster',
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0',
        include=['app.tasks']  # Load your tasks
    )
    celery.config_from_object('celeryconfig')
    return celery

celery = make_celery()

