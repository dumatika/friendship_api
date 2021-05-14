from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from django.utils.translation import ugettext_lazy as _

from users.models import User


class FriendOfFriendSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class FriendSerializer(ModelSerializer):
    friends = FriendOfFriendSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'friends')


class UserSerializer(ModelSerializer):
    friends = FriendSerializer(many=True, read_only=True)
    friends_id = PrimaryKeyRelatedField(many=True, write_only=True, queryset=User.objects.all(), source='friends')

    class Meta:
        model = User
        fields = ('id', 'username', 'friends', 'friends_id')
        read_only_fields = ('username',)

    def validate(self, attrs):
        if self.context['request'].user in attrs['friends']:
            raise ValidationError(
                detail={'friends_id': _('You cannot create friendship with yourself')},
                code='unique'
            )
        return attrs
