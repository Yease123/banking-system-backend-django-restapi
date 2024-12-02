# Generated by Django 5.1.3 on 2024-11-22 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_validateuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validateuser',
            name='otp',
            field=models.CharField(blank=True, default='6163', max_length=4),
        ),
        migrations.CreateModel(
            name='SignupUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=4)),
                ('userdetails', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.registeruser')),
            ],
        ),
    ]
