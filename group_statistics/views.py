from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Group, Event
from .serializers import GetGroupBasicStatisticsSerializer, GetGroupMonthStatisticsSerializer, \
    GetGroupMonthPerYearStatisticsSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


# TODO: Group basic stats

class GroupBasicStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name):

        try:
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

                number_of_members = len(group.members.all())

                # Calculating accumulated amount paid in a group
                all_events_in_a_group = group.events.all()
                event_amounts = [float(event.amount) for event in all_events_in_a_group]
                accumulated_amount_paid = sum(event_amounts)

                # Calculating amounts accumulated by each member
                members = group.members.all()
                members_and_amounts = {}

                for member in members:
                    amounts_by_a_member = group.events.filter(paid_by=member)
                    amounts = [float(event.amount) for event in amounts_by_a_member]
                    members_and_amounts[member.username] = sum(amounts)

                # Build the accumulated_amount_paid_by_users string
                user_amount_strings = [f"{key}'s total contribution is {value} €" for key, value in
                                       members_and_amounts.items()]
                accumulated_amount_paid_by_users = ', '.join(user_amount_strings)

                # Revealing the ownership between the members
                usernames, amounts = [], []
                for key, value in members_and_amounts.items():
                    usernames.append(key)
                    amounts.append(value)

                max_amount_index = amounts.index(max(amounts))
                username_max = usernames.pop(max_amount_index)
                amount_max = amounts.pop(max_amount_index)
                owing = f"{username_max} is owed {amount_max - sum(amounts)} by {usernames[0]}"

                statistics_data = {
                    'number_of_members': number_of_members,
                    'accumulated_amount_paid': accumulated_amount_paid,
                    'accumulated_amount_paid_by_users': accumulated_amount_paid_by_users,
                    'owing': owing
                }

                serializer = GetGroupBasicStatisticsSerializer(data=statistics_data)
                serializer.is_valid()

                response_data = {}
                for key, value in serializer.data.items():
                    if key == "number_of_members":
                        response_data["Number of members"] = value
                    elif key == "accumulated_amount_paid":
                        response_data["Total amount accumulated by your group"] = value
                    elif key == "accumulated_amount_paid_by_users":
                        response_data["How much has each user contributed to your group"] = value
                    elif key == "owing":
                        response_data["Owing status in a group"] = value

                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'Error': 'You are not a group member, as a result you are unauthorized for this action!'},
                    status=status.HTTP_401_UNAUTHORIZED)
        except Group.DoesNotExist:
            return Response({'Error': 'This group does not exist!'}, status=status.HTTP_404_NOT_FOUND)


# TODO: Filtering total stats per month

class GroupMonthStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name, year, month):

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
            months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                      9: "September", 10: "October", 11: "November", 12: "December"}

            report = {}
            monthly_dataset = Event.objects.filter(group=group, date_created__year=year,
                                                   date_created__month=month)
            month_report = {}
            event_types = [event.event_type for event in monthly_dataset]
            for event_type in event_types:
                month_event_report = {}
                event_dataset = monthly_dataset.filter(event_type=event_type)
                particular_event_amount = [float(event.amount) for event in event_dataset]
                type_amounts_sum_month = sum(particular_event_amount)
                month_event_report[f"{event_type}"] = type_amounts_sum_month
                month_report.update(month_event_report)

            serializer = GetGroupMonthStatisticsSerializer(data={"monthly_report": month_report})
            serializer.is_valid()
            response_data = {f"{months[month]}": serializer.data["monthly_report"]}

            return Response(data=response_data, status=status.HTTP_200_OK)


# TODO: Filtering total stats per month in a year
class GroupMonthPerYearStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name, year):

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
            months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                      9: "September", 10: "October", 11: "November", 12: "December"}

            report = {}
            # Get the dataset for the year provided in the url
            yearly_dataset = Event.objects.filter(group=group, date_created__year=year)
            year_report = {}

            # Filter the dataset for monthly check
            for month_number, month_name in months.items():
                monthly_dataset = yearly_dataset.filter(date_created__month=int(month_number))
                # Get all the event types paid for in the looped month
                event_types = [event.event_type for event in monthly_dataset]

                month_report = {}
                # Get the amount paid for every event type in the month
                for event_type in event_types:
                    month_event_report = {}
                    event_dataset = monthly_dataset.filter(event_type=event_type)
                    particular_event_amount = [float(event.amount) for event in event_dataset]
                    type_amounts_sum_month = sum(particular_event_amount)
                    month_event_report[f"{event_type}"] = type_amounts_sum_month
                    month_report.update(month_event_report)

                # Use setdefault to create an empty dictionary if the month_name key doesn't exist
                if month_name not in year_report:
                    year_report[month_name] = {}
                year_report[month_name].update(month_report)

            serializer = GetGroupMonthPerYearStatisticsSerializer(data={"year_report": year_report})
            serializer.is_valid()
            response_data = {f"{year}": serializer.data["year_report"]}

            return Response(data=response_data, status=status.HTTP_200_OK)


# TODO: Filtering every event in a group

class GroupEveryEventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name, year):

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
            months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                      9: "September", 10: "October", 11: "November", 12: "December"}

            report = {}
            # Get the dataset for the year provided in the url
            yearly_dataset = Event.objects.filter(group=group, date_created__year=year)
            year_report = {}

            # Filter the dataset for monthly check
            for month_number, month_name in months.items():
                monthly_dataset = yearly_dataset.filter(date_created__month=int(month_number))
                # Get all the event types paid for in the looped month
                event_types = [event.event_type for event in monthly_dataset]

                month_report = {}
                # Get the amount paid for every event type in the month
                for event_type in event_types:
                    month_event_report = {}
                    event_dataset = monthly_dataset.filter(event_type=event_type)
                    particular_event_amount = [float(event.amount) for event in event_dataset]
                    type_amounts_sum_month = sum(particular_event_amount)
                    month_event_report[f"{event_type}"] = type_amounts_sum_month
                    month_report.update(month_event_report)

                # Use setdefault to create an empty dictionary if the month_name key doesn't exist
                if month_name not in year_report:
                    year_report[month_name] = {}
                year_report[month_name].update(month_report)

            serializer = GetGroupMonthPerYearStatisticsSerializer(data={"year_report": year_report})
            serializer.is_valid()
            response_data = {f"{year}": serializer.data["year_report"]}

            return Response(data=response_data, status=status.HTTP_200_OK)
