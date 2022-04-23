from rest_framework import serializers

from api.models import Worker


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['name', 'jobs', 'coins', 'status']