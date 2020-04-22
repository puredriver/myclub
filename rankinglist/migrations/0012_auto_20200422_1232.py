# Generated by Django 2.2.7 on 2020-04-22 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rankinglist', '0011_merge_20200422_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='path',
        ),
        migrations.RemoveField(
            model_name='player',
            name='id',
        ),
        migrations.AddField(
            model_name='rankinglist',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rankinglist.Club'),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
