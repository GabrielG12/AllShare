from django.contrib import admin
from .models import Group, Event


@admin.register(Group)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', "group_name"]
    ordering = ["group_name"]


@admin.register(Event)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', "event_name"]
    ordering = ["event_name"]
