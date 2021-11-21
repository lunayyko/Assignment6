import datetime

from django.db                       import IntegrityError
from django.contrib.auth             import authenticate, login, logout
from django.contrib.auth.models      import User
from rest_framework                  import status, viewsets
from rest_framework.response         import Response
from rest_framework.decorators       import action
from rest_framework.permissions      import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from drf_spectacular.utils           import extend_schema, OpenApiExample, extend_schema_view

from area.models                     import Area
from user.serializers                import UserSerializer
from vehicle.serializers             import BoardingLogSerializer, DeerLendSerializer, DeerReturnSerializer
from vehicle.models                  import Deer, BoardingLog


@extend_schema_view(
    create=extend_schema(
				tags=['회원'], 
				description='회원 가입을 합니다',
                request=UserSerializer,
                examples=[
                    OpenApiExample(
                    request_only=True,
                    summary='회원가입 예시',
                    name='success_example',
                    value={
                        'username': 'deer',
                        'password': 'deer',
                    }
                ),            
                OpenApiExample(
                    response_only=True,
                    summary='회원가입 성공 예시',
                    name='success_example',
                    value={
                        'id': 1,
                        'username': 'deer',
                        'token': '145d0f4acecb91074b93b64bf7f218822f381b22'
                    },            
                )]  
    ),
    login=extend_schema(
				tags=['회원'], 
				description='로그인을 합니다.',
                request=UserSerializer,
                examples=[
                    OpenApiExample(
                    request_only=True,
                    summary='로그인 예시',
                    name='success_example',
                    value={
                        'username': 'deer',
                        'password': 'deer',
                    },            
                ),
                OpenApiExample(
                    response_only=True,
                    summary='로그인 성공 예시',
                    name='success_example',
                    value={
                        'id': 1,
                        'username': 'deer',
                        'token': '145d0f4acecb91074b93b64bf7f218822f381b22'
                    },            
                )]            
            ),
    logout=extend_schema(
				tags=['회원'], 
				description='로그아웃을 합니다.',
                request=None,
                responses=None,
        ),
    return_deer=extend_schema(
                methods=['POST'],
				tags=['Deer'], 
				description='Deer 반납을 합니다.',
                responses=BoardingLogSerializer,
                request=DeerReturnSerializer,
                examples=[
                    OpenApiExample(
                    request_only=True,
                    summary='반납 예시',
                    name='success_example',
                    value={
                        'deer_name': 'deer1',
                        'use_end_lat': 37.52259182560556,
                        'use_end_lng': 127.01317164880014
                    }
                )]
        ),
        land_deer=extend_schema(
                methods=['POST'],
				tags=['Deer'], 
				description='Deer 대여를 합니다.',
                request=DeerLendSerializer,
                responses=BoardingLogSerializer,
                examples=[
                    OpenApiExample(
                    request_only=True,
                    summary='대여 예시',
                    name='success_example',
                    value={
                        'deer_name': 'deer1',
                    }
                )]		    
        )
)
class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class   = UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return [AllowAny(), ]
        return  [permission() for permission in self.permission_classes]

    def create(self, request):
        """
        POST /users/

        data params
        - username(required)
        - password(required)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response({"error": "A user with that username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        # response data
        data = serializer.data
        data['token'] = user.auth_token.key
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        POST /users/login/

        data params
        - username(required)
        - password(required)
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            data = self.get_serializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data)
        return Response({"error": "Wrong username or wrong password"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        """
        POST /users/logout/
        """
        logout(request)
        return Response()

    @action(detail=False, methods=['POST'])
    def land_deer(self, request):
        """
        대여: POST /users/lend_deer/
            data params
            - deer_name
        """
 
        # deer_name validate
        deer_name = request.data.get('deer_name')
        try:
            deer = Deer.objects.get(name=deer_name)
        except Deer.DoesNotExist:
            return Response({"error": f"deer_name:{deer_name} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        is_user_already_use = BoardingLog.objects.filter(
            in_use=True,
            user=request.user
        ).exists()
        is_deer_already_use = BoardingLog.objects.filter(
            in_use=True,
            deer=deer
        ).exists()

        # 대여가능 상태 validate
        if is_user_already_use or is_deer_already_use:
            return Response({"error": "user or deer already use"}, status=status.HTTP_400_BAD_REQUEST)

        log = BoardingLog.objects.create(
            user=request.user,
            deer=deer,
            in_use=True,
            use_start_at=datetime.datetime.now()
        )

        return Response(BoardingLogSerializer(log).data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['POST'])
    def return_deer(self, request):
        """
        반납: POST /users/return_deer/
            data params
            - deer_name
            - use_end_lat
            - use_end_lng
        """
 
        # deer_name validate
        deer_name = request.data.get('deer_name')
        try:
            deer = Deer.objects.get(name=deer_name)
        except Deer.DoesNotExist:
            return Response({"error": f"deer_name:{deer_name} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if (request.data.get('use_end_lat') is None) or (request.data.get('use_end_lng') is None):
            return Response({"error": "Location not confirmed"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('use_end_lat') < 0 or request.data.get('use_end_lng')  < 0:
            return Response({"error": "Invalid value"}, status=status.HTTP_400_BAD_REQUEST)
            
        use_end_lat = request.data.get('use_end_lat')
        use_end_lng = request.data.get('use_end_lng')   

        # 반납 가능한 상태 validate
        try:
            log = BoardingLog.objects.get(
                in_use=True,
                user=request.user,
                deer=deer,
            )
        except BoardingLog.DoesNotExist:
            return Response({"error": f"user not use deer:{deer_name}"}, status=status.HTTP_400_BAD_REQUEST)

        area = Area.objects.get(id=deer.area_id)
        use_end_at = datetime.datetime.now()

        minute = (use_end_at.timestamp() - log.use_start_at.timestamp()) // 60
        fee = area.basic_fee + minute * area.fee_per_min

        log.in_use = False
        log.use_end_lat = use_end_lat
        log.use_end_lng = use_end_lng
        log.use_end_at = use_end_at
        log.fee = fee
        log.save()

        return Response(BoardingLogSerializer(log).data, status=status.HTTP_200_OK)