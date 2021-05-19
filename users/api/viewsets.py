from django.db.models import OuterRef, Prefetch, Subquery
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from users.api.permissions import UserViewSetPermission
from users.api.serializers import UserDetailedSerializer, UserSerializer
from users.models import Friendship, User


class UserViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (UserViewSetPermission,)

    def get_queryset(self):
        prefetches = []
        if self.action == 'list':
            prefetches += ['friends']
        elif self.action in ('retrieve', 'update', 'partial_update'):
            prefetches += [
                Prefetch(
                    lookup='friends',
                    queryset=User.objects.annotate(
                        created_at=Subquery(
                            Friendship.objects.filter(
                                id=OuterRef('friendships__id'),
                            ).values('created_at')[:1]
                        ),
                    ).distinct().order_by('id'),
                ),
                'friends__friends'
            ]

        queryset = User.objects.prefetch_related(*prefetches)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer

        return UserDetailedSerializer
