from celery import shared_task
from pytube import YouTube
import os
from celery_progress.backend import ProgressRecorder
import requests



@shared_task(bind=True)
def download_progress(self, url):
    try:
        yt = YouTube(url)
        stream = yt.streams.first()
        response = requests.get(stream.url, stream=True)
        total = int(response.headers.get('Content-Length', 0))
        progress_recorder = ProgressRecorder(self)
        chunk_size = 1024
        bytes_received = 0
        homedir = os.path.expanduser("~")
        dirs = homedir + "/Downloads/" + stream.default_filename

        with open(dirs, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                bytes_received += len(chunk)
                progress_recorder.set_progress(bytes_received, total)

    except Exception as _e:
        print(_e)
        raise self.retry(exc=_e, countdown=3)
