from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api
from tzlocal import get_localzone
def start():
	scheduler = BackgroundScheduler({'apscheduler.timezone': get_localzone()})
	scheduler.add_job(schedule_api, 'interval', seconds = 14400,max_instances=1)
	scheduler.start()