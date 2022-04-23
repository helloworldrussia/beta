from django.contrib import admin
from django.urls import path, include

from parsers.views import create_worker

urlpatterns = [
    path('start/', create_worker),
]
