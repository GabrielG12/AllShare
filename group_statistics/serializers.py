from rest_framework import serializers
from groups.models import Group
from django.contrib.auth import get_user_model
from .models import GroupStatistics

User = get_user_model()


class GetGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['group_name', 'members', 'date_created']


class GetGroupBasicStatisticsSerializer(serializers.ModelSerializer):

    number_of_members = serializers.IntegerField()
    accumulated_amount_paid = serializers.DecimalField(max_digits=1000, decimal_places=2, )
    accumulated_amount_paid_by_users = serializers.CharField(max_length=1000)

    class Meta:
        model = GroupStatistics
        fields = ['number_of_members', 'accumulated_amount_paid', 'accumulated_amount_paid_by_users']


"""
class CreateGroupStatistics(serializers.ModelSerializer):

    group = GetGroupSerializer(write_only=True)

    class Meta:
        model = GroupStatistics
        fields = ['group', 'number_of_members', 'accumulated_amount_paid', 'accumulated_amount_paid_by_users']

    def create(self, validated_data):

        # Get the group attribute provided by the request
        group_data = validated_data.pop('group', None)
        group_name = group_data.get('group_name', None)
        members = group_data.get('members', None)

        # Calculating the number of members
        number_of_members = len(members)

        # Get the instance of a group existing
        group = Group.objects.get(group_name=group_name)

        # Calculating accumulated amount paid in a group
        all_events_in_a_group = group.events.all()
        event_amounts = [float(event.amount) for event in all_events_in_a_group]
        accumulated_amount_paid = sum(event_amounts)

        # Calculating amounts accumulated by each member
        members = [member.username for member in group.members.all()]
        members_and_amounts = {}

        for mem in members:
            amounts_by_a_member = group.events.filter(paid_by=mem)
            amounts = [float(event.amout) for event in amounts_by_a_member]
            members_and_amounts[mem] = sum(amounts)
        accumulated_amount_paid_by_users = ""

        for key, value in members_and_amounts.items():
            accumulated_amount_paid_by_users += f"{key}'s total payment is {value}, "
            if key == list(members_and_amounts.keys())[-1]:
                accumulated_amount_paid_by_users += f"{key}'s total payment is {value}."

        # Create an instance of the GroupStatistics model
        instance = GroupStatistics.objects.create(group=group_name, number_of_members=number_of_members, accumulated_amount_paid=accumulated_amount_paid, accumulated_amount_paid_by_users=accumulated_amount_paid_by_users)
        return instance
"""
