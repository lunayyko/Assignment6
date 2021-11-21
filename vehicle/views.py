from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from vehicle.models import Deer


class DeerViewSet(viewsets.GenericViewSet):
    queryset = Deer.objects.all()
    # serializer_class =
    permission_classes = [IsAuthenticated()]

    def list(self,request):
        """
        GET /deers/
        """
        pass