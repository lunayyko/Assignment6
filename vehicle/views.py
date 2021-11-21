from rest_framework                  import generics
from rest_framework.permissions      import AllowAny
from rest_framework.pagination       import LimitOffsetPagination
from drf_spectacular.utils           import extend_schema, extend_schema_view

from vehicle.models                  import Deer
from vehicle.serializers             import DeerSerializer


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20

@extend_schema_view(
    get=extend_schema(
				tags=['Deer'], 
				description='Deer를 조회 합니다.',
		),
)
class DeerListView(generics.ListAPIView):
    queryset           = Deer.objects.all()
    serializer_class   = DeerSerializer
    permission_classes = [AllowAny]
    pagination_class   = CustomLimitOffsetPagination