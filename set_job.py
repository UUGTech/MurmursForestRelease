import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
import os

scheduler = BlockingScheduler(timezone="Asia/Tokyo")

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cmd = "python3 " + dir_path + "/recent_tweets_predict.py"
    subprocess.call(cmd.split())
    return

if __name__ == "__main__":
    for i in range(12):
        scheduler.add_job(main, 'cron', minute=i*5, misfire_grace_time=50)
    scheduler.start()