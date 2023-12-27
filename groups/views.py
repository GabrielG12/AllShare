from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Group, Event
from .serializers import GroupCreateSerializer, EventCreateSerializer, GetGroupEventsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
import random

User = get_user_model()


class GroupCreateView(CreateAPIView):

    queryset = Group.objects.all()
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        # Retrieves an instance of the serializer provided in the serializer_class
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # The create method in the serializer handles the instance creation
            serializer.create(validated_data=serializer.validated_data)
            return Response({'Message': f"Group {serializer.validated_data['group_name']} created successfully"})
        else:
            # Custom message when data is not valid
            error_messages = [
                "Invalid data. Please check your input.",
                "Something went wrong with the provided data.",
                "Oops! The data doesn't meet the validation criteria.",
            ]
            random_message = random.choice(error_messages)
            return Response(data={'message': random_message}, status=400)


class EventCreateView(CreateAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Manually set date_created to the provided date (if any)
        date_created = request.data.get('date_created')
        if date_created:
            serializer.validated_data['date_created'] = date_created

        self.perform_create(serializer)
        return Response({'Message': f"Event {serializer.validated_data['event_name']} created successfully"})


# TODO: Filtering every event in a group
class GetAllGroupEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name):

        group = Group.objects.get(group_name=group_name)

        auth_header = request.headers["Authorization"]
        token_string = auth_header.split(" ")[1]
        token = AccessToken(token_string)

        # Print the entire token payload
        token_payload = token.payload

        # Extract the user_id from the token payload
        user_id = token.payload.get("user_id")

        group_members = [member.username for member in group.members.all()]

        try:
            user = User.objects.get(id=user_id)
            token_username = user.username
        except User.DoesNotExist:
            token_username = None
        token_username = token_username.strip()

        if token_username is not None and token_username in group_members:
            event_dataset = Event.objects.filter(group=group)
            events = {}
            for i in range(len(event_dataset)):
                event = event_dataset[i]
                amount = float(event.amount)
                event_name = str(event.event_name)
                event_type = str(event.event_type)
                paid_by = str(event.paid_by)
                date = str(event.date_created)
                dict_ = {f"{event_name}": {"Type": event_type, "Amount paid:": amount, "Paid by": paid_by, "Date": date}}
                events.update(dict_)

            serializer = GetGroupEventsSerializer(data={"events": events})
            serializer.is_valid()
            response_data = {"Events": serializer.data["events"]}
            return Response(data=response_data, status=status.HTTP_200_OK)


# TODO: Filtering every event in a group on a certain day

class GetGroupEventsOnADateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name, year, month, day):

        group = Group.objects.get(group_name=group_name)

        auth_header = request.headers["Authorization"]
        token_string = auth_header.split(" ")[1]
        token = AccessToken(token_string)

        # Print the entire token payload
        token_payload = token.payload

        # Extract the user_id from the token payload
        user_id = token.payload.get("user_id")

        group_members = [member.username for member in group.members.all()]

        try:
            user = User.objects.get(id=user_id)
            token_username = user.username
        except User.DoesNotExist:
            token_username = None
        token_username = token_username.strip()

        if token_username is not None and token_username in group_members:
            event_dataset = Event.objects.filter(group=group, date_created__year=year, date_created__month=month, date_created__day=day)
            events = {}
            for i in range(len(event_dataset)):
                event = event_dataset[i]
                amount = float(event.amount)
                event_name = str(event.event_name)
                event_type = str(event.event_type)
                paid_by = str(event.paid_by)
                dict_ = {f"{event_name}": {"Type": event_type, "Amount paid:": amount, "Paid by": paid_by}}
                events.update(dict_)

            serializer = GetGroupEventsSerializer(data={"events": events})
            serializer.is_valid()
            response_data = {"Events": serializer.data["events"]}
            return Response(data=response_data, status=status.HTTP_200_OK)
