# Generated by Django 2.2.16 on 2021-11-09 08:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20211109_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=uuid.uuid4, max_length=36),
        ),
    ]
