# Generated by Django 3.1.7 on 2021-03-17 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='texts',
        ),
    ]
