# Generated by Django 4.1.7 on 2023-03-20 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_menuelement_menu_child'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuelement',
            name='menu_parent',
        ),
    ]
