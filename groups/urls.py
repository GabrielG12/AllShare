from django.urls import path
from .views import GroupCreateView, EventCreateView, GetAllGroupEventsView, GetGroupEventsOnADateView

urlpatterns = [
    path('create/', GroupCreateView.as_view(), name='create-group'),
    path('events/create/', EventCreateView.as_view(), name='create-event'),
    path('<str:group_name>/get_events/all/', GetAllGroupEventsView.as_view(), name='get-all-group-events'),
    path('<str:group_name>/get_events/<int:year>__<int:month>__<int:day>/', GetGroupEventsOnADateView.as_view(), name='get-all-group-events'),
]

