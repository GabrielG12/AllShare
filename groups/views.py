from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Group, Event
from .serializers import GroupCreateSerializer, EventCreateSerializer
from rest_framework.permissions import IsAuthenticated
import random


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

    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        # Retrieves an instance of the serializer provided in the serializer_class
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # The create method in the serializer handles the instance creation
            serializer.create(validated_data=serializer.validated_data)
            return Response({'Message': f"Event {serializer.validated_data['event_name']} created successfully"})
        else:
            # Custom message when data is not valid
            error_messages = [
                "Invalid data. Please check your input.",
                "Something went wrong with the provided data.",
                "Oops! The data doesn't meet the validation criteria.",
            ]
            random_message = random.choice(error_messages)
            return Response(data={'message': random_message}, status=400)
