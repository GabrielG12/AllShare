from django.urls import path
from .views import GroupCreateView

urlpatterns = [
    path('group/create/', GroupCreateView.as_view(), name='create-group'),
]

