from rest_framework import generics, status
from .serializers import SignUpSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user


class SignUpView(generics.GenericAPIView):

    permission_classes = []
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        data = request.data
        serializer = SignUpSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {"Message": f'User {data["username"]} has been created!'}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)
            response = {"Message": f"Login for user {user.username} was successful!",
                        "Tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data="Invalid username or password!", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request):

        content = {
            "Username": str(request.user),
            "Access token": str(request.auth),
        }
        return Response(data=content, status=status.HTTP_200_OK)

