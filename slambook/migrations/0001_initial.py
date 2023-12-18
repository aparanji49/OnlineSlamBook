# Generated by Django 4.2.6 on 2023-11-02 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField(blank=True, max_length=15)),
                ('status', models.CharField(max_length=50)),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
