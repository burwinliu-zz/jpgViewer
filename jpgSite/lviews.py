from django.contrib import messages
from django.contrib.auth import forms
from django.shortcuts import render


def register(request):
    if request.method == 'POST':
        f = forms.UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return forms.redirect('register')

    else:
        f = forms.UserCreationForm()

    return render(request, 'registration/register.html', {'form': f})
