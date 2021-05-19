from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class Friendship(models.Model):
    initiator = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
    )

    partner = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='friendships'
    )

    created_at = models.DateTimeField(
        default=timezone.now
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

    def __str__(self):
        return f'Friendship {self.id} of initiator {self.initiator_id} with partner {self.partner_id}'


class User(AbstractUser):
    friends = models.ManyToManyField(
        to='self',
        symmetrical=True,
        through=Friendship,
    )
