# Generated by Django 3.0.8 on 2020-08-18 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taco',
            name='tacos_for',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='taco_history', to='home.User'),
        ),
    ]
