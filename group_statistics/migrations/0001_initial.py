# Generated by Django 5.0 on 2023-12-24 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_members', models.IntegerField(default=0)),
                ('accumulated_amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=2, max_length=1000000000)),
                ('accumulated_amount_paid_by_users', models.CharField(default=0, max_length=1000000000)),
                ('owing', models.CharField(default=0, max_length=1000000000)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_info', to='groups.group')),
            ],
        ),
    ]
