from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Friendship, User


class FriendshipInline(admin.TabularInline):
    model = Friendship
    fk_name = 'initiator'
    fields = ('id', 'initiator', 'partner')
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [FriendshipInline, ]
