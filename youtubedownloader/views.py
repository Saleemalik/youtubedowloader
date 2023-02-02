from django.shortcuts import render
from pytube import YouTube
import os

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
    global url
    if request.method == 'POST':
        try:
            download_progress.delay(url)
            return render(request, 'done.html')
        except Exception as e:
                return render(request, 'error.html')
