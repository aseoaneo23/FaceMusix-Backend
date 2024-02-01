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
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    id_usuario_amigo = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_amigo', related_name='amigos_id_usuario_amigo_set')

    class Meta:
        managed = False
        db_table = 'amigos'


class Artistas(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    genero = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artistas'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Canciones(models.Model):
    título = models.CharField(max_length=100, blank=True, null=True)
    duración = models.TimeField(blank=True, null=True)
    album = models.ForeignKey(Albumes, models.DO_NOTHING)
    artista = models.ForeignKey(Artistas, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'canciones'


class Cancionplaylist(models.Model):
    playlist = models.ForeignKey('Playlist', models.DO_NOTHING)
    cancion = models.ForeignKey(Canciones, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cancionplaylist'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Playlist(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlist'


class Ratings(models.Model):
    author = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='author')
    comments = models.CharField(max_length=1000, blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)
    cancion = models.ForeignKey(Canciones, models.DO_NOTHING)

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
