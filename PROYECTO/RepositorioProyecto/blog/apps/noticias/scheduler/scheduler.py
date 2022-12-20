from django.contrib.sessions.models import Session
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
import sys
from ..models import Noticia


def restart_new_views():
    news = Noticia.objects.all()
    Session.objects.all().delete()
    for new in news:
        new.views_week = 0
        new.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(restart_new_views, 'interval',
                      hours=168, name='clean_accounts', jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
