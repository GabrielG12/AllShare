from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Group
from .serializers import GetGroupBasicStatisticsSerializer
from rest_framework_simplejwt.tokens import AccessToken


class GroupBasicStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name):

        try:
            group = Group.objects.get(group_name=group_name)

            auth_header = request.headers["Authorization"]
            try:
                # Extract the token from the Authorization header
                token_string = auth_header.split(" ")[1]
                token = AccessToken(token_string)
            except Exception:
                return False

            token_payload = token.payload
            print("Token Payload:", token_payload)

            # Extract the username from the token payload
            token_username = token.payload.get("username")
            print("Token ID:", token_username)

            group_members = [member.username for member in group.members.all()]
            print("Group Members:", group_members)

            if token_username is not None:
                group_members = [member.username for member in group.members.all()]
                print("Group Members:", group_members)

                if token_username in group_members:
                    print("User is a group member")
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

                statistics_data = {
                    'number_of_members': number_of_members,
                    'accumulated_amount_paid': accumulated_amount_paid,
                    'accumulated_amount_paid_by_users': accumulated_amount_paid_by_users
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

                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                return Response({'Error': 'You are not a group member, as a result you are unauthorized for this action!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Group.DoesNotExist:
            return Response({'Error': 'This group does not exist!'}, status=status.HTTP_404_NOT_FOUND)

