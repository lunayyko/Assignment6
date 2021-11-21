from django.urls import path, include
from rest_framework.routers import SimpleRouter

from vehicle.views import DeerViewSet

app_name = 'vehicle'

router = SimpleRouter()

router.register('deers', DeerViewSet, basename='vehicles')

urlpatterns = [
    path('', include((router.urls)))
]
