# Generated by Django 2.2 on 2019-05-24 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_auto_20190513_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposittransaction',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
