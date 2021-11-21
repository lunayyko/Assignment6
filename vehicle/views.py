from datetime                        import datetime

from rest_framework                  import status, viewsets, response
from rest_framework.decorators       import action
from rest_framework.permissions      import IsAuthenticated, AllowAny
from rest_framework.pagination       import LimitOffsetPagination

from vehicle.models                  import Deer, BoardingLog
from vehicle.serializers             import DeerSerializer


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class VehicleViewSet(viewsets.GenericViewSet):
    queryset           = Deer.objects.all()
    serializer_class   = DeerSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'deer_name'
    pagination_class   = CustomLimitOffsetPagination

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
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


    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)