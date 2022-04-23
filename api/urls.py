from django.contrib import admin
from django.urls import path, include

from api.views import ListWorkers

urlpatterns = [
    path('workers/', ListWorkers.as_view()),
]