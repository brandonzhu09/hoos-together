# Generated by Django 4.1.2 on 2022-10-15 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventName', models.TextField(max_length=25)),
                ('eventTime', models.DateTimeField()),
                ('eventDesc', models.TextField(max_length=100)),
            ],
        ),
    ]