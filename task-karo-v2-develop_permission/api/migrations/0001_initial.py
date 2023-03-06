# Generated by Django 4.1.3 on 2023-01-27 08:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=12, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('social_id', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_image', models.TextField(blank=True, null=True)),
                ('social_type', models.CharField(blank=True, max_length=255, null=True)),
                ('device_info', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(max_length=7)),
                ('relation', models.CharField(blank=True, max_length=255, null=True)),
                ('alternative_mobile_number', models.CharField(blank=True, max_length=255, null=True)),
                ('alternative_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_mobile_verified', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('reference_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('token_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deleted_by_user', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_user', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(primary_key=True, serialize=False)),
                ('city_name', models.CharField(blank=True, max_length=255, null=True)),
                ('area_name', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.AutoField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(blank=True, max_length=255, null=True)),
                ('country_code', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('family_id', models.AutoField(primary_key=True, serialize=False)),
                ('relation', models.CharField(blank=True, max_length=250, null=True)),
                ('family_head', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family_head_user_family', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('location_name', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('latitude', models.CharField(max_length=255, null=True)),
                ('longitude', models.CharField(max_length=255, null=True)),
                ('active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.city')),
                ('family_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.family')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('charge_id_or_reference_id', models.CharField(max_length=100, null=True)),
                ('amount', models.FloatField(default=False)),
                ('payment_status', models.BooleanField()),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('scheduler_id', models.AutoField(primary_key=True, serialize=False)),
                ('scheduler_time', models.CharField(blank=True, max_length=255, null=True)),
                ('scheduler_title', models.CharField(blank=True, max_length=255, null=True)),
                ('scheduler_body', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service_provider',
            fields=[
                ('service_provider_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_provider_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_number', models.CharField(max_length=12, unique=True)),
                ('service_type', models.CharField(blank=True, max_length=255, null=True)),
                ('active', models.BooleanField(default=True)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('alternative_mobile_number', models.CharField(max_length=12, null=True)),
                ('tag', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user_service_provider', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deleted_by_user_service_provider', to=settings.AUTH_USER_MODEL)),
                ('family_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.family')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.location')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_user_service_provider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SmsAudit',
            fields=[
                ('sms_audit_id', models.AutoField(primary_key=True, serialize=False)),
                ('fast2sms_account_id', models.CharField(max_length=255, null=True)),
                ('fast2sms_sms_id', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('body', models.TextField()),
                ('purpose', models.TextField()),
                ('from_number', models.CharField(max_length=25, null=True)),
                ('to_number', models.CharField(max_length=255, null=True)),
                ('fast2sms_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscription_Plan',
            fields=[
                ('subscription_plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('duration_days', models.IntegerField(max_length=100, null=True)),
                ('subscription_plan_name', models.CharField(max_length=255, null=True)),
                ('price', models.FloatField()),
                ('max_num_of_location', models.CharField(max_length=12, null=True)),
                ('max_num_of_appliance', models.CharField(max_length=12, null=True)),
                ('max_num_of_services', models.CharField(max_length=12, null=True)),
                ('max_num_of_family_member', models.CharField(max_length=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Subscription',
            fields=[
                ('user_subscription_id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('expiry_date', models.DateTimeField(null=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('max_num_of_location', models.CharField(max_length=12, null=True)),
                ('max_num_of_appliance', models.CharField(max_length=12, null=True)),
                ('max_num_of_services', models.CharField(max_length=12, null=True)),
                ('max_num_of_family_member', models.CharField(max_length=12, null=True)),
                ('family_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.family')),
                ('payment_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.payment')),
                ('subscription_plan_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.subscription_plan')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=255, null=True)),
                ('start_datetime', models.DateTimeField(auto_now_add=True)),
                ('end_datetime', models.DateTimeField()),
                ('task_description', models.CharField(max_length=255, null=True)),
                ('task_attechments', models.FileField(null=True, upload_to='')),
                ('active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('assagned_member_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user_task', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deleted_by_user_task', to=settings.AUTH_USER_MODEL)),
                ('family_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.family')),
                ('location_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.location')),
                ('scheduler_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.scheduler')),
                ('service_provider_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.service_provider')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_user_task', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_id', models.AutoField(primary_key=True, serialize=False)),
                ('state_name', models.CharField(blank=True, max_length=255, null=True)),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.country')),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('permission_id', models.AutoField(primary_key=True, serialize=False)),
                ('permission', models.JSONField()),
                ('family_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.family')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.role')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OTPs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=15, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='state_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.state'),
        ),
        migrations.AddField(
            model_name='city',
            name='country_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.country'),
        ),
        migrations.AddField(
            model_name='city',
            name='state_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.state'),
        ),
        migrations.CreateModel(
            name='Appliances',
            fields=[
                ('appliance_id', models.AutoField(primary_key=True, serialize=False)),
                ('appliance_type', models.CharField(blank=True, max_length=255, null=True)),
                ('bought_from', models.CharField(blank=True, max_length=255, null=True)),
                ('appliance_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_number', models.CharField(max_length=12, unique=True)),
                ('alternativ_mobile_number', models.CharField(max_length=255, null=True)),
                ('price', models.FloatField()),
                ('invoice_number', models.CharField(max_length=255, null=True)),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('billing_email', models.EmailField(max_length=254)),
                ('billing_name', models.CharField(max_length=255, null=True)),
                ('billing_mobile_number', models.CharField(max_length=12)),
                ('warranty_last_date', models.CharField(max_length=255, null=True)),
                ('product_image', models.ImageField(default='product/default.png', null=True, upload_to='')),
                ('is_amc_service_available', models.BooleanField(null=True)),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('contact_person_name', models.CharField(max_length=255, null=True)),
                ('amc_phone_number', models.CharField(max_length=255, null=True)),
                ('support_email', models.CharField(max_length=255, null=True)),
                ('amc_service_address', models.CharField(max_length=255, null=True)),
                ('service_time_period', models.CharField(max_length=255, null=True)),
                ('appliance_note', models.CharField(max_length=255, null=True)),
                ('upload_invoice_pdf_img', models.ImageField(default='product/default.png', null=True, upload_to='')),
                ('active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user_appliance', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deleted_by_user_appliance', to=settings.AUTH_USER_MODEL)),
                ('family_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.family')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.location', verbose_name=('location',))),
                ('service_provider_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.service_provider')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_user_appliance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
