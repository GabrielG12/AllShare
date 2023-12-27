from rest_framework import serializers
from .models import Group, Event
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class GetUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username']


class GetGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField()

    class Meta:
        model = Group
        fields = ['group_name']


class GroupCreateSerializer(serializers.ModelSerializer):

    members = serializers.ListField(write_only=True)

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'members', 'date_created']

    def create(self, validated_data):

        # Take out the members from the data provided
        members_data = validated_data.pop('members', [])

        # Creates instance of the Group model without the members data
        instance = Group.objects.create(**validated_data)

        # Check whether the username exists in the User DB
        for username in members_data:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                # Get that username from the User DB
                user = User.objects.get(username=username)
                # Add it to the members value
                instance.members.add(user)
            else:
                raise serializers.ValidationError(f"User with username '{username}' does not exist.")
        # Return the created Group instance with the validated data
        return instance


class GroupUpdateSerializer(serializers.ModelSerializer):

    members = serializers.ListField(write_only=True)

    class Meta:
        fields = ['group_name', 'members']

    def update(self, instance, validated_data):

        # Get the value from the group_name attribute from the PUT/PATCH request and set the instance attribute value to this value
        instance.group_name = validated_data.get('group_name', instance.group_name)
        instance.members = validated_data.get('members', instance.members)
        members_data = validated_data.get('members', [])

        # Check whether the username exists in the User DB
        for username in members_data:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                # Get that username from the User DB
                user = User.objects.get(username=username)
                if user not in instance.members.all():
                    # Add it to the members value
                    instance.members.add(user)
                else:
                    continue
            else:
                raise serializers.ValidationError(f"User with username '{username}' does not exist.")

        instance.save()
        return instance


class EventCreateSerializer(serializers.ModelSerializer):
    group = GetGroupSerializer(write_only=True)
    paid_by = GetUserSerializer(write_only=True)

    class Meta:
        model = Event
        fields = ['id', 'group', 'event_name', 'event_type', 'paid_by', 'amount', 'date_created']
        read_only_fields = ['id', 'date_created']

    def create(self, validated_data):

        group_data = validated_data.pop('group', None)
        paid_by_data = validated_data.pop('paid_by', None)

        group_name = group_data.get('group_name', None)
        if group_name:
            try:
                group = Group.objects.get(group_name=group_name)

                if group:
                    # Retrieve user if it exists
                    username = paid_by_data.get('username', None)
                    user = User.objects.filter(username=username).first()

                    if user:
                        if user in group.members.all():
                            instance = Event.objects.create(group=group, paid_by=user, **validated_data)
                            return instance
                        else:
                            raise serializers.ValidationError("The user is not a member of the group.")
                    else:
                        raise serializers.ValidationError(f"User with username '{username}' does not exist.")
                else:
                    raise serializers.ValidationError("This group does not exist or you're not a member.")
            except ObjectDoesNotExist:
                raise serializers.ValidationError("This group does not exist or you're not a member.")
        else:
            raise serializers.ValidationError("Group name is required.")


class GetGroupEventsSerializer(serializers.Serializer):
    events = serializers.DictField()
