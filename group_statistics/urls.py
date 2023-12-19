from django.urls import path
from .views import GroupBasicStatisticsAPIView

urlpatterns = [
    path('<str:group_name>/', GroupBasicStatisticsAPIView.as_view(), name="get-group-stats"),
]
