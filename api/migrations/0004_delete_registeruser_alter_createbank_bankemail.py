# Generated by Django 5.1.3 on 2024-11-18 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_registeruser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='registerUser',
        ),
        migrations.AlterField(
            model_name='createbank',
            name='bankemail',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]