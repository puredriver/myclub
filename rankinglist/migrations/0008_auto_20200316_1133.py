# Generated by Django 2.2.7 on 2020-03-16 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rankinglist', '0007_auto_20200316_0813'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name': 'Spiel', 'verbose_name_plural': 'Spiele'},
        ),
        migrations.AlterModelOptions(
            name='ranking',
            options={'ordering': ['position'], 'verbose_name': 'Position', 'verbose_name_plural': 'Positionen'},
        ),
        migrations.AlterModelOptions(
            name='rankinglist',
            options={'verbose_name': 'Rangliste', 'verbose_name_plural': 'Ranglisten'},
        ),
        migrations.RemoveField(
            model_name='player',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='player',
            name='lastname',
        ),
        migrations.AlterField(
            model_name='match',
            name='playedat',
            field=models.DateTimeField(verbose_name='Spieldatum'),
        ),
        migrations.AlterField(
            model_name='match',
            name='playerone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playerone', to=settings.AUTH_USER_MODEL, verbose_name='Spieler 1 (Sieger)'),
        ),
        migrations.AlterField(
            model_name='match',
            name='playertwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playertwo', to=settings.AUTH_USER_MODEL, verbose_name='Spieler 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='rankinglist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rankinglist.Rankinglist', verbose_name='Rangliste'),
        ),
        migrations.AlterField(
            model_name='match',
            name='set1playerone',
            field=models.IntegerField(default=0, verbose_name='Satz1 - Spieler 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='set1playertwo',
            field=models.IntegerField(default=0, verbose_name='Satz1 - Spieler 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='set2playerone',
            field=models.IntegerField(default=0, verbose_name='Satz2 - Spieler 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='set2playertwo',
            field=models.IntegerField(default=0, verbose_name='Satz2 - Spieler 2'),
        ),
        migrations.AlterField(
            model_name='match',
            name='set3playerone',
            field=models.IntegerField(default=0, verbose_name='Satz3 - Spieler 1'),
        ),
        migrations.AlterField(
            model_name='match',
            name='set3playertwo',
            field=models.IntegerField(default=0, verbose_name='Satz3 - Spieler 2'),
        ),
    ]