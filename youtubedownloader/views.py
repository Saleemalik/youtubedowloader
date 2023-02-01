from django.shortcuts import render
from pytube import YouTube
import os

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
    homedir = os.path.expanduser("~")
    dirs = homedir + "/Downloads"
    if request.method == 'POST':
        video = YouTube(url).streams.filter(progressive=True).all()
        try:
            if "360p" in [vid.resolution for vid in video]:
                YouTube(url).streams.get_by_resolution("360p").download(dirs)
            else:
                YouTube(url).streams.get_lowest_resolution().download(dirs)
            return render(request, 'done.html')
        except Exception as e:
                return render(request, 'error.html')
