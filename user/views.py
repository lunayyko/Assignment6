import datetime

from rest_framework                  import status, viewsets
from rest_framework.response         import Response
from rest_framework.decorators       import action
from rest_framework.permissions      import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from django.db                       import IntegrityError
from django.contrib.auth             import authenticate, login, logout
from django.contrib.auth.models      import User

from area.models                     import Area
from user.serializers                import UserSerializer
from vehicle.serializers             import BoardingLogSerializer
from vehicle.models                  import Deer, BoardingLog


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated(), ]

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return [AllowAny(), ]
        return self.permission_classes

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

    @action(detail=True, methods=['POST', 'DELETE'])
    def deer(self, request, pk):
        """
        대여: POST /users/{user_id}/deer/
            data params
            - deer_name

        반납: DELETE /users/{user_id}/deer/
            data params
            - deer_name
            - use_end_lat
            - use_end_lng
        """
        # authorization validate
        if int(pk) != request.user.id:
            return Response({"error": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        # deer_name validate
        deer_name = request.data.get('deer_name')
        try:
            deer = Deer.objects.get(name=deer_name)
        except Deer.DoesNotExist:
            return Response({"error": f"deer_name:{deer_name} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "POST":

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

        if request.method == "DELETE":
            
            if (request.data.get('use_end_lat') is not None) or (request.data.get('use_end_lng') is not None):
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