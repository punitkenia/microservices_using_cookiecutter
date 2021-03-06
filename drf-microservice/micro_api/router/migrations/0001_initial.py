# Generated by Django 2.2.10 on 2020-11-05 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RouterDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sapid', models.CharField(max_length=100)),
                ('hostname', models.CharField(max_length=100)),
                ('loopback', models.CharField(max_length=100)),
                ('mac_address', models.CharField(max_length=100)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'router_details',
            },
        ),
    ]
