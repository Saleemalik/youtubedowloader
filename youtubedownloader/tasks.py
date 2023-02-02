from celery import shared_task
from pytube import YouTube
import os


@shared_task(bind=True)
def download_progress(self, url):
    homedir = os.path.expanduser("~")
    dirs = homedir + "/Downloads"
    video = YouTube(url).streams.filter(progressive=True).all()
    try:
        if "360p" in [vid.resolution for vid in video]:
            YouTube(url).streams.get_by_resolution("360p").download(dirs)
        else:
            YouTube(url).streams.get_lowest_resolution().download(dirs)
    except Exception as _e:
        print(_e)
        raise self.retry(exc=_e, countdown=3)