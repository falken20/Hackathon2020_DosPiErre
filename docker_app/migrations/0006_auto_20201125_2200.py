# Generated by Django 3.1.3 on 2020-11-25 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docker_app', '0005_auto_20201125_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='retoitem',
            name='points_1',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='retoitem',
            name='points_2',
            field=models.IntegerField(default=25),
        ),
        migrations.AddField(
            model_name='retoitem',
            name='points_3',
            field=models.IntegerField(default=10),
        ),
    ]
