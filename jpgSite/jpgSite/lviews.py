from django.contrib import messages
from django.contrib.auth import forms
# from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.contrib.staticfiles.urls import static
# from django.views.generic import TemplateView
# from django.http import StreamingHttpResponse, HttpResponseNotFound

import cv2
import threading
import os


from django.http import StreamingHttpResponse
from jpgSite import settings
from os.path import join
# from django.template import Context, Template


def register(request):
    if request.method == 'POST':
        print(request.POST)
        f = forms.UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('home')

    else:
        f = forms.UserCreationForm()

    return render(request, 'registration/register.html', {'form': f})


def camera(request):
    url = settings.MEDIA_URL+'/images/test.png'
    root = settings.MEDIA_ROOT+'/images/test.png'
    test_url = os.path.join(settings.MEDIA_ROOT, os.path.join('images', 'test.png'))
    return render(request, 'camera.html',
                  {'media_url': settings.MEDIA_ROOT,
                   'images': static(url, document_root=root),
                   'test': test_url})


def test(request):
    return render(request, 'test.html')


class VideoCamera(object):
    def __init__(self):
        self._video = cv2.VideoCapture(0)
        (self._grabbed, self._frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self._grabbed, self._frame) = self.video.read()


def helper():
    try:
        web_camera = VideoCamera()
        while True:
            frame = web_camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    finally:
        if web_camera:
            web_camera.__del__()


def render_request_stream(request):
    return StreamingHttpResponse(helper(),
                                 content_type="multipart/x-mixed-replace;boundary=frame")


def render_request_simple(request):
    simple = cv2.VideoCapture(0)
    return_value, image = simple.read()
    cv2.imwrite('opencv.png', image)
    del simple
    return render(request, 'render_simple.html')
