from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, data):
        try:
            User.objects.get(username=data.get('email'))
            raise serializers.ValidationError(
                {'non_field_errors': ['Account already exists with ' + data.get('email')]})
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=data.get('email'),
                # when the user is created, the username field is overwritten by email field
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, obj):
        user = authenticate(username=obj.get('email'), password=obj.get('password'))
        if user:
            if user.is_active:
                return user
        else:
            try:
                user = User.objects.get(username=obj.get('email'))
            except:
                user = None

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('Please Activate your account.')
        raise serializers.ValidationError('Incorrect username or password')
