# Generated by Django 4.2.6 on 2023-11-02 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slambook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='friends',
            name='phone',
            field=models.IntegerField(blank=True),
        ),
    ]