# Generated by Django 3.0.4 on 2020-05-03 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collections',
            name='mov_name',
        ),
        migrations.AddField(
            model_name='collections',
            name='mov_id',
            field=models.IntegerField(null=True),
        ),
    ]
