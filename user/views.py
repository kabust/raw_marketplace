from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from user.models import User
from user.serializers import UserSerializer, UserRegistrationSerializer, PasswordUpdateSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope)
    default_serializer_class = UserSerializer
    serializer_classes = {
        "register": UserRegistrationSerializer,
        "set_password": PasswordUpdateSerializer,
        "me": UserSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(detail=False, url_path="me", methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Password updated successfully.'})
