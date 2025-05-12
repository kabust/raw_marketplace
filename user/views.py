from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from user.models import User
from user.serializers import UserSerializer, UserRegistrationSerializer, PasswordUpdateSerializer


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.AllowAny, TokenHasReadWriteScope]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "register":
            return UserRegistrationSerializer
        elif self.action == "set_password":
            return PasswordUpdateSerializer
        elif self.action == "me":
            return UserSerializer

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer_class()
        serialized_user = serializer(request.user)
        return Response(serialized_user.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = self.get_serializer_class()
        serializer.is_valid(request.data, raise_exception=True)
        serialized_user = serializer(request.user)
        user = serialized_user.save()
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        serializer = self.get_serializer_class()
        serializer.is_valid(request.data, raise_exception=True)
        serialized_user = serializer(request.user)
        serialized_user.save()
        return Response({'message': 'Password updated successfully.'})
