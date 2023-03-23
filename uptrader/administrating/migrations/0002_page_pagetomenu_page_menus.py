# Generated by Django 4.1.7 on 2023-03-23 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_remove_menuelement_menu_parent'),
        ('administrating', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='PageToMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField()),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.menu')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrating.page')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='menus',
            field=models.ManyToManyField(through='administrating.PageToMenu', to='menu.menu'),
        ),
    ]
