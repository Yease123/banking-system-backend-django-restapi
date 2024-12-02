# Generated by Django 5.1.3 on 2024-11-18 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_registeruser_accountno'),
    ]

    operations = [
        migrations.CreateModel(
            name='validateUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('accountno', models.CharField(max_length=100)),
                ('otp', models.CharField(blank=True, default='7560', max_length=4)),
            ],
        ),
    ]