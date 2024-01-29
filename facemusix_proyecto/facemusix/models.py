# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Albumes(models.Model):
    título = models.CharField(max_length=100, blank=True, null=True)
    año = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'albumes'


class Amigos(models.Model):
    id_usuario = models.ForeignKey('Usuarios', on_delete=models.CASCADE, db_column='id_usuario')
    id_usuario_amigo = models.ForeignKey('Usuarios', on_delete=models.CASCADE, db_column='id_usuario_amigo', related_name='amigos_id_usuario_amigo_set')

    class Meta:
        managed = False
        db_table = 'amigos'


class Artistas(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    genero = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artistas'


class Canciones(models.Model):
    título = models.CharField(max_length=100, blank=True, null=True)
    duración = models.TimeField(blank=True, null=True)
    album = models.ForeignKey(Albumes, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artistas, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'canciones'


class Cancionplaylist(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE )
    cancion = models.ForeignKey(Canciones, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'cancionplaylist'


class Playlist(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlist'


class Ratings(models.Model):
    author = models.ForeignKey(Artistas, on_delete=models.CASCADE, db_column='author')
    comments = models.CharField(max_length=1000, blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)
    cancion = models.ForeignKey(Canciones, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ratings'


class Usuarios(models.Model):
    url_avatar = models.CharField(max_length=1000, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    nombre_usuario = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    passwd = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
