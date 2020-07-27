# Generated by Django 3.0.8 on 2020-07-27 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date_created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='System.Status'),
        ),
    ]
