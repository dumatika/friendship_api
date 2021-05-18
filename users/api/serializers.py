from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from users.api.errors import FRIENDSHIP_WITH_YOURSELF_ERROR
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


class UserDetailedSerializer(ModelSerializer):
    friends = FriendSerializer(many=True, read_only=True)
    friends_ids = PrimaryKeyRelatedField(many=True, write_only=True, queryset=User.objects.all(), source='friends')

    class Meta:
        model = User
        fields = ('id', 'username', 'friends', 'friends_ids')
        read_only_fields = ('username',)

    def validate(self, attrs):
        if self.context['request'].user in attrs['friends']:
            raise ValidationError(detail={'friends_ids': FRIENDSHIP_WITH_YOURSELF_ERROR})
        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'friends')
