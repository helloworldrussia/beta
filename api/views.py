from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from api.models import Worker
from api.serializers import WorkerSerializer


class ListWorkers(ListAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

    class Meta:
        model = Worker