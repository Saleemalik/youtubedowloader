from django.shortcuts import render
from pytube import YouTube
import os
from youtube.celery import app
from django.http import JsonResponse


from .tasks import download_progress
# Create your views here.

def index(request):
    return render(request, 'index.html')


def download(request):
    global url
    url = request.GET.get('url')
    yt = YouTube(url)
    video = []
    video = yt.streams.filter(progressive=True).all()
    context = {
        "video": video,
        "embed": url.replace("watch?v=", "embed/"),
        "title": yt.title
    }
    return render(request, 'download.html', context)


def start_download(request):
    '''start downloading'''
    global url
    if request.method == 'POST':
        try:
            task = download_progress.delay(url)
            return render(request, 'done.html', {'task_id': task.task_id})
        except Exception as e:
                return render(request, 'error.html')


def stop_download(request):
    '''To Cancelled the already executing task'''
    task_id = eval(request.body).get('task_id')
    app.control.terminate(task_id)
    return JsonResponse({'result': 'cancelled'})
