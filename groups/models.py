from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):

    group_name = models.CharField(max_length=255, null=False)
    members = models.ManyToManyField(User, max_length=255, related_name='group_memberships')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.group_name


class Event(models.Model):

    event_types = [
        ("Gas", "Gas"),
        ("Bills", "Bills"),
        ("Groceries", "Groceries"),
        ("Parking", "Parking"),
        ("Dinning/Going out", "Dinning/Going out"),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events', null=False)
    event_name = models.CharField(max_length=255, null=False)
    event_type = models.CharField(max_length=255, choices=event_types, null=False)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_events')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateField(auto_now_add=True, null=False)

    def __str__(self):
        return self.event_name
