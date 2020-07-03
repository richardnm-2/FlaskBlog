import os
import flaskblog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import time
import shutil


def print_time(msg):
    print(msg)
    print(time.strftime('%H:%M:%S'))


def clearfolder(folder_path):
    folder = folder_path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def bg_scheduler(function, args):
    dirname = os.path.dirname(flaskblog.__file__)
    clear_path = os.path.join(dirname, (r'static/profile_pics/temp'))
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=lambda: function(clear_path),
        # func=lambda: print_time('a'),
        trigger=IntervalTrigger(seconds=2),
        id='printing_time_job',
        name='Print time every 2 seconds',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
