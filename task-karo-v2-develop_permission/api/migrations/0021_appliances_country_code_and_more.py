# Generated by Django 4.1.3 on 2023-03-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_user_is_profile_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliances',
            name='country_code',
            field=models.CharField(default='+91', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='service_provider',
            name='country_code',
            field=models.CharField(default='+91', max_length=20, null=True),
        ),
    ]
