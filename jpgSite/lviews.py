from django.contrib import messages
from django.contrib.auth import forms
# from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect


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
    return render(request, 'camera.html')
