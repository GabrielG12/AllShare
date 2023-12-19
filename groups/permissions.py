from rest_framework import permissions
from .models import Group
from rest_framework_simplejwt.tokens import AccessToken


class IsGroupMember(permissions.BasePermission):

    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        # Check if the request contains a valid token
        if "Authorization" not in request.headers:
            return False

        auth_header = request.headers["Authorization"]
        try:
            # Extract the token from the Authorization header
            token_string = auth_header.split(" ")[1]
            token = AccessToken(token_string)
        except Exception:
            return False

        # Extract the username from the token payload
        token_username = token.payload.get("username")

        group_members = [member.username for member in obj.members.all()]

        return token_username in group_members
