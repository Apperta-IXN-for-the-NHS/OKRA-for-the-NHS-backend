import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from app.trending_service import update_trending, update_related
# this class is used to automatically make a request to the VPS web service to update trending and similarity score


def update_trending_scheduler():
    print("processing trending updates")
    response = update_trending()


def update_related_scheduler():
    print("processing related updates")
    response = update_related()


def start_scheduler():
    print("scheduler is running")
    # update_related_scheduler()
    scheduler = BlockingScheduler()
    scheduler.add_job(update_trending, 'interval', hours=24)
    scheduler.add_job(update_related_scheduler, 'interval', hours=168)
    scheduler.start()


