"""jpgSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from jpgSite import settings
from jpgSite import lviews

# from django.urls import path


urlpatterns = [
    # Login and user management
    url(r'^login/?$', views.LoginView.as_view(), name='login'),
    url(r'^logout/?$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/?$', lviews.register, name='register'),
    url(r'^admin/?', admin.site.urls),
    url(r'^password_reset/?', views.PasswordResetView.as_view(), name='password_reset'),

    # Development stuff
    url(r'^test/?', lviews.test),

    # Actual pages
    url(r'^view_cam/?', lviews.camera, name='view_cam'),
    url(r'^render/?', lviews.render_request_simple, name='render'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^view_stream/?', lviews.view_stream, name='view_stream')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
