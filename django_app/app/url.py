from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from . import view

# from .view import index

urlpatterns = [
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),
    path('admin/', admin.site.urls),
    path('index/', view.index),
]
