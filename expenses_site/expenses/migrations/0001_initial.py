# Generated by Django 5.1.2 on 2024-10-17 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField()),
                ('name', models.CharField(max_length=30)),
                ('contact_number', models.CharField(max_length=13)),
            ],
        ),
    ]
