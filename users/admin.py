from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q

from users.models import Friendship, User


# TODO
class FriendshipInline(admin.TabularInline):
    model = Friendship
    fk_name = 'initiator'
    fields = ('id', 'initiator', 'partner')
    extra = 0

    def get_queryset(self, request):
        return Friendship.objects.filter(
            Q(partner=request.user) | Q(initiator=request.user)
        )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [FriendshipInline, ]
