from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token


class SignUpSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=10, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate(self, data):

        # CHECK IF THE USERNAME ALREADY EXISTS
        username_exists = User.objects.filter(username=data['username']).exists()
        if username_exists:
            raise ValidationError(f"Username {data['username']} has already been used. Try using another unique username!")

        return super().validate(data)

    def create(self, validated_data):

        # HASHING THE PASSWORD
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)

        return user
