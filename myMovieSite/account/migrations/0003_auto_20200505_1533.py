# Generated by Django 3.0.4 on 2020-05-05 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200503_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='content_type',
        ),
        migrations.AlterField(
            model_name='comments',
            name='user_name',
            field=models.CharField(max_length=50),
        ),
    ]
