# Generated by Django 4.2.7 on 2024-07-25 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pole', '0012_camille'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ete_exo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.DateField()),
                ('exercice', models.CharField(max_length=30)),
                ('duree', models.IntegerField()),
                ('joueuse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pole.personne')),
            ],
        ),
    ]
