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


class DeerLendSerializer(serializers.Serializer):
    deer_name = serializers.CharField()


class DeerReturnSerializer(serializers.Serializer):
    deer_name = serializers.CharField()
    use_end_lat = serializers.DecimalField(max_digits=17, decimal_places=14)
    use_end_lng = serializers.DecimalField(max_digits=17, decimal_places=14)