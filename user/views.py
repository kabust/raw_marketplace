from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from user.serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
