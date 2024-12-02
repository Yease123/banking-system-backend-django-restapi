# Generated by Django 5.1.3 on 2024-11-18 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_delete_registeruser_alter_createbank_bankemail'),
    ]

    operations = [
        migrations.CreateModel(
            name='registerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('useremail', models.EmailField(max_length=254)),
                ('accountno', models.CharField(max_length=100, unique=True)),
                ('amount', models.CharField(max_length=100)),
                ('userbank', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.createbank')),
            ],
        ),
    ]
