# Generated by Django 2.2 on 2019-04-09 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Middlename',
            new_name='middlename',
        ),
    ]
