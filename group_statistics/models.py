from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Event, Group

User = get_user_model()


class GroupStatistics(models.Model):

    group = models.ForeignKey(Group, related_name='group_info', on_delete=models.CASCADE)
    number_of_members = models.IntegerField(default=0)
    accumulated_amount_paid = models.DecimalField(max_length=1000000000, default=0, decimal_places=2, max_digits=2)
    accumulated_amount_paid_by_users = models.CharField(max_length=1000000000, default=0)



