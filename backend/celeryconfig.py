from celery.schedules import crontab

beat_schedule = {
    'daily-reminder-every-evening': {
        'task': 'app.tasks.send_daily_reminders',
        'schedule': crontab(hour = 10,minute=0),
    },
    'monthly-report-every-1st': {
        'task': 'app.tasks.send_monthly_report',
        'schedule': crontab(day_of_month='1', hour=9, minute=0),
    }
}

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
timezone = 'Asia/Kolkata'
enable_utc = True
beat_schedule = beat_schedule
