# Generated by Django 3.2 on 2022-12-20 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0005_noticia_comentarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='comentarios',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='views_total',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='views_week',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
