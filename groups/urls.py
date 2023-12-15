from django.urls import path
from .views import GroupCreateView, EventCreateView

urlpatterns = [
    path('create/', GroupCreateView.as_view(), name='create-group'),
    path('events/create/', EventCreateView.as_view(), name='create-event'),
]

