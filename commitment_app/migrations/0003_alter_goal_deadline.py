# Generated by Django 5.1.1 on 2024-10-30 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment_app', '0002_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
