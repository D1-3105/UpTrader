# Generated by Django 4.1.7 on 2023-03-20 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='elements',
            field=models.ManyToManyField(blank=True, to='menu.menuelement'),
        ),
    ]
