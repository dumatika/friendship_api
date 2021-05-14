from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.permissions import UserViewSetPermission
from users.serializers import UserDetailedSerializer, UserSerializer


class UserViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (UserViewSetPermission,)

    def get_queryset(self):
        queryset = User.objects.prefetch_related('friends')

        if self.action == 'list':
            queryset.prefetch_related('friends__friends')

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer

        return UserDetailedSerializer
