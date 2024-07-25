# Generated by Django 4.2.7 on 2024-07-16 12:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pole', '0011_alter_personne_options_remove_personne_carte_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.DateField()),
                ('exercice', models.CharField(max_length=30)),
                ('plaisir', models.IntegerField()),
                ('effort', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('joueuse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pole.personne')),
            ],
        ),
    ]
