# Generated by Django 3.2 on 2021-04-16 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0003_topic_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
