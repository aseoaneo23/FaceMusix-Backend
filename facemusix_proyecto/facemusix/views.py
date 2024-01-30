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
            elif check_password(password, Usuarios.objects.get(email=email).passwd) == 0:
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


#Función buscar Canciones
@csrf_exempt
def buscar_canciones(request):

    if request.method == "GET":
        query_canciones = Canciones.objects.all()  # Se recogen todas la canciones en una QUERY
        query_search = request.GET.get("search", None)  # Se recoge el parámetro enviado SEARCH

        if query_search:
            query_canciones = query_canciones.filter(título__icontains=query_search)  # Filtrado de canciones por titulo

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

            query_ratings = Ratings.objects.all().filter(cancion=cancion.id)

            json_cancion = {
                "título": cancion.título,
                "duración": cancion.duración,
                "album": cancion.album.título,
                "rating": {
                    query_ratings.authon,
                    query_ratings.comments,
                    query_ratings.stars
                }
            }
            json_canciones.append(json_cancion)

        return JsonResponse({"canciones": json_canciones, "total": paginador.count, "page": page},
                             status=200)

    else:
        return JsonResponse({"error": "No se ha enviado un GET"}, status=405)



