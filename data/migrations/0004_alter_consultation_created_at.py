# Generated by Django 3.2.20 on 2023-07-12 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_alter_consultation_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
