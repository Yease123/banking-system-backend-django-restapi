# Generated by Django 5.1.3 on 2024-11-18 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_registeruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='userbank',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.createbank'),
        ),
    ]