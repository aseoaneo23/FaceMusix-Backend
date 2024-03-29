# Generated by Django 5.0.1 on 2024-01-30 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Albumes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('título', models.CharField(blank=True, max_length=100, null=True)),
                ('año', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'albumes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Amigos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'amigos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Artistas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('genero', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'artistas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Canciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('título', models.CharField(blank=True, max_length=100, null=True)),
                ('duración', models.TimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'canciones',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cancionplaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'cancionplaylist',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'playlist',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(blank=True, max_length=1000, null=True)),
                ('stars', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ratings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_avatar', models.CharField(blank=True, max_length=1000, null=True)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('nombre_usuario', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('passwd', models.CharField(blank=True, max_length=100, null=True)),
                ('token', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'usuarios',
                'managed': False,
            },
        ),
    ]
