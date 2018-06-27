# Generated by Django 2.0.1 on 2018-04-27 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_administratorinfo_newsinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='NpticeInfo',
            fields=[
                ('notice_id', models.AutoField(primary_key=True, serialize=False)),
                ('notice_title', models.CharField(max_length=120)),
                ('notice_details', models.CharField(max_length=600)),
                ('notice_time', models.DateField(max_length=20)),
            ],
        ),
    ]