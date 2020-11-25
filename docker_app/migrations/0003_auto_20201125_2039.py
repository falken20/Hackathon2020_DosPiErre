# Generated by Django 3.1.3 on 2020-11-25 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docker_app', '0002_auto_20201125_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyitem',
            name='logo_url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='promotionitem',
            name='type',
            field=models.CharField(choices=[('D', 'Discount'), ('M', 'Merchandising'), ('T', 'Free tickets'), ('R', 'Regalo')], max_length=1),
        ),
    ]
