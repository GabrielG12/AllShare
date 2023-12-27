from django.contrib import admin
from .models import Group, Event
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Group)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', "group_name", "get_members", "date_created"]
    ordering = ["group_name"]

    def get_members(self, obj):
        return ', '.join([user.username for user in obj.members.all()])

    get_members.short_description = 'Members'


@admin.register(Event)
class UserAdmin(admin.ModelAdmin):
    list_display = ["group", "event_name", "event_type", "paid_by", "get_amount", "date_created"]
    ordering = ["event_name"]

    def get_amount(self, obj):
        amount = obj.amount
        return amount

    get_amount.short_description = 'Amount [€]'
