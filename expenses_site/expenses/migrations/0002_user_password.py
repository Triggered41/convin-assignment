# Generated by Django 5.1.2 on 2024-10-17 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
