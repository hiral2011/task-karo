# Generated by Django 4.1.3 on 2023-01-31 05:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='user_id',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription_plan',
            name='duration_days',
            field=models.IntegerField(null=True),
        ),
    ]
