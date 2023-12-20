from django.urls import path
from .views import GroupBasicStatisticsAPIView

urlpatterns = [
    path('<str:group_name>/basic/', GroupBasicStatisticsAPIView.as_view(), name="get-basic-group-stats"),
]
