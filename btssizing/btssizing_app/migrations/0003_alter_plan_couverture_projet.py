# Generated by Django 4.0.4 on 2022-06-04 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('btssizing_app', '0002_alter_plan_couverture_nb_sites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan_couverture',
            name='projet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='btssizing_app.projet'),
        ),
    ]