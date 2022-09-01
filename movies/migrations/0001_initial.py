# Generated by Django 4.1 on 2022-09-01 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("name", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "_id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "numberInStock",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                (
                    "dailyRentalRate",
                    models.DecimalField(
                        blank=True, decimal_places=1, max_digits=4, null=True
                    ),
                ),
                (
                    "_id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="movies.genre",
                    ),
                ),
            ],
        ),
    ]