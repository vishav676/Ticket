# Generated by Django 2.2 on 2020-07-31 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0016_auto_20200729_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile.png', null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('priority', models.CharField(choices=[('Critical', 'Critical'), ('High', 'High'), ('Normal', 'Normal'), ('Low', 'Low')], default='Normal', max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Progress', 'Progress'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_bugs', to='System.Task')),
            ],
        ),
    ]
