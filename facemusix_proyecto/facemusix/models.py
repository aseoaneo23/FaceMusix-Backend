# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Amigos(models.Model):
    id_usuario = models.OneToOneField('Usuarios', models.DO_NOTHING, db_column='id_usuario', primary_key=True)  # The composite primary key (id_usuario, id_usuario_amigo) found, that is not supported. The first column is selected.
    id_usuario_amigo = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_amigo', related_name='amigos_id_usuario_amigo_set')

    class Meta:
        managed = False
        db_table = 'amigos'
        unique_together = (('id_usuario', 'id_usuario_amigo'),)


class Canciones(models.Model):
    título = models.CharField(max_length=100, blank=True, null=True)
    duración = models.TimeField(blank=True, null=True)
    album = models.ForeignKey('lbumes', models.DO_NOTHING, blank=True, null=True)
    ratings = models.ForeignKey('Ratings', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'canciones'


class Cancionplaylist(models.Model):
    playlist_id = models.IntegerField(primary_key=True)  # The composite primary key (playlist_id, cancion_id) found, that is not supported. The first column is selected.
    cancion_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cancionplaylist'
        unique_together = (('playlist_id', 'cancion_id'),)


class Playlist(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlist'


class Ratings(models.Model):
    author = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratings'


class Usuarios(models.Model):
    url_avatar = models.CharField(max_length=1000, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    nombre_usuario = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    passwd = models.CharField(max_length=100, blank=True, null=True)
    artista = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class lbumes(models.Model):
    título = models.CharField(max_length=100, blank=True, null=True)
    año = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'álbumes'
