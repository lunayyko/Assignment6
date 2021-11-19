from .models import Deer, BoardingLog
from rest_framework import serializers


class DeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deer
        fields = "__all__"

class BoardingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingLog
        fields = "__all__"
