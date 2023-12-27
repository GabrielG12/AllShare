import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):

    group_name = models.CharField(max_length=255, null=False)
    members = models.ManyToManyField(User, max_length=255, related_name='group_memberships')
    date_created = models.DateField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.group_name


class Event(models.Model):

    event_types = [
        ("Gas", "Gas"),
        ("Gifts", "Gifts"),
        ("Bills", "Bills"),
        ("Electricity", "Electricity"),
        ("Energy", "Energy"),
        ("Home/Rent/Maintenance", "Home/Rent/Maintenance"),
        ("Car expenses", "Car expenses"),
        ("Groceries", "Groceries"),
        ("Parking", "Parking"),
        ("Dinning/Going out", "Dinning/Going out"),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events', null=False)
    event_name = models.CharField(max_length=255, null=False)
    event_type = models.CharField(max_length=255, choices=event_types, null=False)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_events')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.event_name
