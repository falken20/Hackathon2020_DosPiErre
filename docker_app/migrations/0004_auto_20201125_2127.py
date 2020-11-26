# Generated by Django 3.1.3 on 2020-11-25 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docker_app', '0003_auto_20201125_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyitem',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, default='0', max_digits=9),
        ),
        migrations.AddField(
            model_name='companyitem',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, default='0', max_digits=9),
        ),
        migrations.AddField(
            model_name='companyitem',
            name='zip_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]