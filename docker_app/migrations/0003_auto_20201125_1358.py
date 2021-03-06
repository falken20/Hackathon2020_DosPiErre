# Generated by Django 3.1.3 on 2020-11-25 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docker_app', '0002_boyitem_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boyitem',
            name='address',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='boyitem',
            name='city',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='boyitem',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='boyitem',
            name='password',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='boyitem',
            name='province',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='boyitem',
            name='surname',
            field=models.CharField(blank=True, default='', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='boyitem',
            name='user',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='companyitem',
            name='address',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='companyitem',
            name='company',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='companyitem',
            name='id_company',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='companyitem',
            name='sector',
            field=models.CharField(max_length=20),
        ),
    ]
