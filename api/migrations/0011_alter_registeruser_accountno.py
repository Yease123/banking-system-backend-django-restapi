# Generated by Django 5.1.3 on 2024-11-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_registeruser_accountno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='accountno',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
