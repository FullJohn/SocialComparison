# Generated by Django 3.2.9 on 2021-12-04 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialComp', '0003_auto_20211202_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='channel',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='description',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='thumbnail',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='title',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='url',
            field=models.CharField(max_length=300),
        ),
    ]