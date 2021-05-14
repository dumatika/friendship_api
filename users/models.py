from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class Friendship(models.Model):
    initiator = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
    )

    partner = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='friendships_partner'
    )

    created_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('initiator', 'partner'),
                name='unique_initiator_partner_constraint'
            ),
            models.UniqueConstraint(
                fields=('partner', 'initiator'),
                name='unique_partner_initiator_constraint'
            ),
            models.CheckConstraint(
                check=~Q(initiator=F('partner')),
                name='friendship_with_yourself_constraint'
            )
        )


class User(AbstractUser):
    friends = models.ManyToManyField(
        to='self',
        symmetrical=True,
        through=Friendship,
    )
