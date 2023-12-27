from django.urls import path
from .views import GroupBasicStatisticsAPIView, GroupMonthStatisticsView, GroupMonthPerYearStatisticsView

urlpatterns = [
    path('<str:group_name>/basic/', GroupBasicStatisticsAPIView.as_view(), name="get-basic-group-stats"),
    path('<str:group_name>/totals/<int:year>__<int:month>/', GroupMonthStatisticsView.as_view(), name="get-month-group-stats"),
    path('<str:group_name>/totals/<int:year>/', GroupMonthPerYearStatisticsView.as_view(), name="get-year-group-stats"),
]
