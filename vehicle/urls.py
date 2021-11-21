from django.urls            import path

from vehicle.views          import DeerListView

urlpatterns = [
    path('deers/', DeerListView.as_view()),
]
