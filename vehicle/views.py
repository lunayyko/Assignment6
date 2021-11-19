from datetime                        import datetime

from rest_framework                  import status, viewsets, response
from rest_framework.decorators       import action
from rest_framework.permissions      import IsAuthenticated, AllowAny

from vehicle.models                  import Deer, BoardingLog
from user.serializers                import UserSerializer
from vehicle.serializers             import DeerSerializer, BoardingLogSerializer

class VehicleViewSet(viewsets.GenericViewSet):
    quertset           = Deer.objects.all()
    serializer_class   = DeerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field       = 'deer_name'

    @action(detail=True, methods=['POST'])
    def rent(self, request, deer_name):
        if BoardingLog.objects.filter(user_id = request.user.id, in_use=True).exists():
            return response.Response("One Deer Allowed", status=status.HTTP_400_BAD_REQUEST)
        if BoardingLog.objects.filter(deer__name = deer_name, in_use=True).exists():
            return response.Response("Already In Use", status=status.HTTP_400_BAD_REQUEST)

        BoardingLog.objects.create(
            user_id = request.user.id,
            deer = Deer.objects.get(name = deer_name),
            in_use = True,
            use_start_at = datetime.now()
        )
        return response.Response("Start Using Deer", status=status.HTTP_200_OK)


