from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from authentication import serializers


class Login(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # logging in
        login(request, user)
        return Response({
            'token': AuthToken.objects.create(user)[1],
            'user_id': user.id
        })


class Register(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'response': 'User registration successful. Continue to login'
        })


class Logout(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request._auth.delete()
        return Response(status=HTTP_200_OK)
