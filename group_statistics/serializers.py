from rest_framework import serializers
from groups.models import Group, Event
from django.contrib.auth import get_user_model
from .models import GroupStatistics
from groups.serializers import GetGroupSerializer, GetUserSerializer

User = get_user_model()


class CreateGroupStatistics(serializers.ModelSerializer):

    class Meta:
        model = GroupStatistics
        fields = "__all__"

    def validate(self, attrs):
