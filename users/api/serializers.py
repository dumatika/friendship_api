from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from users.api.errors import FRIENDSHIP_WITH_YOURSELF_ERROR
from users.models import User


class FriendOfFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class FriendSerializer(serializers.ModelSerializer):
    friends = FriendOfFriendSerializer(many=True)
    created_at = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ('id', 'username', 'created_at', 'friends',)


class UserDetailedSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(many=True, read_only=True)
    friends_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True,
        queryset=User.objects.all(),
        source='friends'
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'friends', 'friends_ids')
        read_only_fields = ('username',)

    def validate(self, attrs):
        if self.context['request'].user in attrs['friends']:
            raise ValidationError(detail={'friends_ids': FRIENDSHIP_WITH_YOURSELF_ERROR})
        return attrs

    def update(self, instance, validated_data):
        """
        Default `.update()` method, but with overwritten friends' m2m assignment and return object annotation
        :param instance:
        :param validated_data:
        :return:
        """
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            if attr == 'friends':
                print('friends update', value)
                field.set(value, through_defaults={'created_at': timezone.now()})

        return self.context['view'].get_object()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'friends')
