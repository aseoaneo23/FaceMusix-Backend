from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from .models import Amigos, Canciones, Cancionplaylist, Playlist, Usuarios, Ratings
from django.core.paginator import Paginator


def verify_token(request):
    token = request.META.get("HTTP_AUTHORIZATION", None)
    if not token:
        return JsonResponse({"error", "No se ha enviado ningún token"}, status=401), None
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        payload = jwt.decode(token, "tu_clave_secreta", algorithm="HS256")
        return None, payload
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error", "El token ha expirado!"}, status=401), None
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Token no válido!"}, status=401), None


@csrf_exempt
# Función para el registro de usuarios
def Registro(request):
    # Si la petición no es POST mandar error, sólo puede ser un POST.
    if request.method != "POST":
        return JsonResponse({"error": "no es un método POST"}, status=405)
    else:
        # Comprobamos que se pasen los campos todos cubiertos y las contraseñas coincidan
        if request.POST.get("name") == None or request.POST.get("username") == None or request.POST.get(
                "email") == None or request.POST.get("password") == None or request.POST.get("confirmpassword") == None:
            return JsonResponse({"ALERTA": "DEBES CUBRIR TODOS LOS CAMPOS"}, status=400)
        elif request.POST.get("password") != request.POST.get("confirmpassword"):
            return JsonResponse({"ALERTA": "LAS CONTRASEÑAS NO COINCIDEN"}, status=400)

        # Se comprueba que no existe ningún usuario con ese email o usuario

        username = request.POST.get("username")
        email = request.POST.get("email")
        # Consultas para comprobar si existe el usuario
        queryEmails = Usuarios.objects.filter(email=email).count()
        queryUsernames = Usuarios.objects.filter(nombre_usuario=username).count()
        # Comprobaciones para evitar redundancia
        if (queryEmails > 0):
            return JsonResponse({"Mensaje": "el email ya esta registrado"})
        elif (queryUsernames > 0):
            return JsonResponse({"Mensaje": "el nombre de usuario ya esta en uso"})
        else:
            name = request.POST.get("name")
            password_withouthash = request.POST.get("password")
            password = make_password(password_withouthash)
            # Inserciones de los datos de usuario nuevos
            usuario = Usuarios(nombre=name, nombre_usuario=username, email=email, passwd=password)
            usuario.save()
            return JsonResponse({"Mensaje": "Registro exitoso"}, status=201)


@csrf_exempt
# Función para el login y logout.
def login_logout(request):
    if request.method == 'POST':
        json_respuesta = json.loads(request.body)

        email = json_respuesta["email"]
        password = json_respuesta["password"]

        if email == "" or password == "":
            return JsonResponse({"error": "Los campos no pueden estar vacíos."}, status=400)
        else:
            queryEmail = Usuarios.objects.filter(email=email).count()
            print(password)
            print(Usuarios.objects.get(email=email).passwd)
            print(check_password(password, Usuarios.objects.get(email=email).passwd))
            if queryEmail == 0:
                return JsonResponse({"error": "Email incorrecto."}, status=405)
            elif check_password(password, Usuarios.objects.get(email=email).passwd) == 1:
                return JsonResponse({"error": "Contraseña incorrecta."}, status=405)
            else:
                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                    'iat': datetime.datetime.utcnow(),
                }

                token = jwt.encode(payload, 'tu_clave_secreta', algorithm='HS256')
                Usuarios.objects.filter(email=email).update(token=token)
                return JsonResponse({"token": token}, status=201)
    elif request.method == "DELETE":
        token = request.META.get('HTTP_AUTHORIZATION', None)
        queryToken = Usuarios.objects.filter(token=token).count()

        if token == "" or queryToken == 0:
            return JsonResponse({"error": "Token no enviado o inexistente."}, status=400)
        else:
            Usuarios.objects.filter(token=token).update(token="")
            return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"error": "No se ha pasado un DELETE o POST"})


@csrf_exempt
# Función para el listado o creación de playlists.
def Playlists(request):
    # Guardar datos de token y comprobar que se esté pasando ese token
    token = request.headers.get("sessionToken", None)

    if token == None:
        return JsonResponse({"ALERTA": "NO SE HA PASADO UN TOKEN DE USUARIO"}, status=401)

    # Endpoint crear playlist
    # Si el método es post es una creación de una playlist
    if request.method == "POST":
        playlistName = request.POST.get("playlistName")

        if playlistName != "":

            queryPlaylists = Playlist.objects.filter(nombre=playlistName).count()
            if queryPlaylists > 0:
                return JsonResponse({"ALERTA": "YA EXISTE UNA PLAYLIST CON EL NOMBRE INTRODUCIDO"}, status=409)
            else:
                newPlaylist = Playlist(nombre=playlistName)
                newPlaylist.save()
                return JsonResponse({"INFO": "SE HA CREADO SATISFACTORIAMENTE LA PLAYLIST"}, status=201)
        else:
            return JsonResponse({"ALERTA": "EL NOMBRE DE LA PLAYLIST NO PUEDE QUEDAR VACIO"}, status=400)

    # Endpoint listar playlists
    # si el método es GET, se listan las playlists
    elif request.method == "GET":

        queryPlaylists = Playlist.objects.all()

        finalResponse = []

        for everyPlaylist in queryPlaylists:
            dicc = {}
            dicc["Nombre"] = everyPlaylist.nombre
            finalResponse.append(dicc)

        return JsonResponse(finalResponse, safe=False)

    else:
        return JsonResponse({"ALERTA": "NO HAS MANDADO UN MÉTODO ADECUADO. PRUEBA CON POST O GET"})


@csrf_exempt
# funcion para eliminar plahylist
def playlistById(request, playlistid):
    # Guardar datos de token y comprobar que se esté pasando ese token
    # token = request.headers.get("sessionToken",None)

    # if token == None:
    #   return JsonResponse({"ALERTA":"NO SE HA PASADO UN TOKEN DE USUARIO"},status=401)

    # Endpoint borrar playlist por id
    # Comprobamos el método
    if request.method == "DELETE":

        checkidQuery = Playlist.objects.filter(id=playlistid).count()

        # Comprobamos que exista la playlist a borrar
        if checkidQuery == 0:
            return JsonResponse({"ERROR": "LA PLAYLIST CON EL ID SELECCIONADO NO EXISTE"}, status=409)
        else:
            deleteQuery = Playlist.objects.filter(id=playlistid).delete()
            return JsonResponse({"INFO": "PLAYLIST ELIMINADA SATISFACTORIAMENTE"}, status=200)

    # Endpoint buscar playlist por id para ver su contenido
    elif request.method == "GET":
        # Query que devuelve un array de objetos que son canciones con sus campos. Si un campo de ellas es foreign,
        # también será un objeto. MIRAR *
        queryPlaylist = Cancionplaylist.objects.filter(playlist=playlistid).select_related('cancion')

        songs_list = []
        # Recorremos el array y guardamos en un diccionario los datos de las canciones y en un array a su vez.
        for cancion in queryPlaylist:
            song = {
                'nombre': cancion.cancion.título,
                'duración': cancion.cancion.duración,
                'album': cancion.cancion.album.título,  # queremos el titulo del album y album: foreign en canciones.
                'artista': cancion.cancion.artista.nombre
            }
            songs_list.append(song)

        # print(songs_list)

        return JsonResponse(songs_list, safe=False)


@csrf_exempt
def buscar_canciones(request):
    if request.method == "GET":
        query_canciones = Canciones.objects.all()  # Se recogen todas la canciones en una QUERY
        query_search = request.GET.get("search", None)  # Se recoge el parámetro enviado SEARCH

        if query_search:
            query_canciones = query_canciones.filter(título__icontains=query_search)  # Filtrado de canciones por titulo
            if query_canciones.count() == 0:
                return JsonResponse({"info": "No hay ninguna canción asociada"}, status=200)
            # Ordenación por defecto en título o por parámetro sort.
            sort_by = request.GET.get("sort", "título")
            query_canciones.order_by(sort_by)

            # Paginación
            paginador = Paginator(query_canciones, request.GET.get("limit", 10))  # Paginador de 10 pág. por defecto
            page = request.GET.get("pag", 1)  # Primera página por defecto

            # Generación de json
            canciones = paginador.get_page(page)  # Se escoge la página que se inserta en el json
            json_canciones = []
            json_cancion = {}
            for cancion in canciones:  # Iteración for para cada canción en canciones

                query_ratings = Ratings.objects.filter(cancion=cancion.id)

                for rating in query_ratings:
                    json_cancion = {
                        "título": cancion.título,
                        "duración": cancion.duración,
                        "album": cancion.album.título,
                        "rating": {
                            "autor": rating.author.nombre_usuario,
                            "comentario": rating.comments,
                            "stars": rating.stars
                        }
                    }
                    json_canciones.append(json_cancion)  # Se añade el json de cada canción en el json_canciones

            return JsonResponse({"canciones": json_canciones, "total": paginador.count, "page": page},
                                status=200)
        else:
            return JsonResponse({"error": "No se envió parámetro search"}, status=400)
    else:
        return JsonResponse({"error": "No se ha enviado un GET"}, status=405)


@csrf_exempt
def cancion_ID(request, cancionId):

    if request.method == "GET":
        # Se comprueba si existe una canción con el ID envaido
        if Canciones.objects.filter(id=cancionId).count() < 1:
            return JsonResponse({"message": "No existe ninguna canción"}, status=409)

        # Query de canciones filtradas por ID
        query_canciones = Canciones.objects.filter(id=cancionId)[0]
        # Query de ratings asociados a la canción
        json_ratings = Ratings.objects.filter(cancion=cancionId)[0]

        json_cancion = {
            "titulo": query_canciones.título,
            "duración": query_canciones.duración,
            "album": query_canciones.album.título,
            "artista": query_canciones.artista.nombre,
            "ratings": {
                "autor": json_ratings.author.nombre_usuario,
                "comentario": json_ratings.comments,
                "stars": json_ratings.stars,
            }
        }

        return JsonResponse({"cancion": json_cancion}, status=200)
    else:
        return JsonResponse({"error": "No se ha enviado un GET"}, status=400)
