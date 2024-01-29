from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from .models import Amigos,Canciones,Cancionplaylist,Playlist,Usuarios,Albumes,Ratings,Artistas


@csrf_exempt
# Función para el registro de usuarios
def Registro(request):
    # Si la petición no es POST mandar error, sólo puede ser un POST.
    if request.method != "POST":

        return JsonResponse({"error":"método HTTP no soportado"}, status=405)
    else:
        #Comprobamos que se pasen los campos todos cubiertos y las contraseñas coincidan
        if request.POST.get("name") == "" or request.POST.get("username") == "" or request.POST.get("email") == "" or request.POST.get("password") == "" or request.POST.get("confirmpassword") == "":
            return JsonResponse({"ALERTA":"DEBES CUBRIR TODOS LOS CAMPOS"},status=400)
        elif request.POST.get("password") != request.POST.get("confirmpassword"):
            return JsonResponse({"ALERTA": "LAS CONTRASEÑAS NO COINCIDEN"}, status=400)

        # Se comprueba que no existe ningún usuario con ese email o usuario

        username = request.POST.get("username")
        email = request.POST.get("email")
        # Consultas para comprobar si existe el usuario
        queryEmails = Usuarios.objects.filter(email=email).count()
        queryUsernames = Usuarios.objects.filter(nombre_usuario=username).count()

        #Comprobaciones para evitar redundancia
        if(queryEmails > 0):
            return JsonResponse({"Mensaje":"el email ya esta registrado"},status=409)
        elif(queryUsernames > 0):
            return JsonResponse({"Mensaje":"el nombre de usuario ya esta en uso"},status=409)
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
            eturn JsonResponse({"error": "Los campos no pueden estar vacíos."}, status=400)
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
#Función para el listado o creación de playlists.
def Playlists(request):
    #Guardar datos de token y comprobar que se esté pasando ese token
    #token = request.headers.get("sessionToken",None)

    #if token == None:
     #   return JsonResponse({"ALERTA":"NO SE HA PASADO UN TOKEN DE USUARIO"},status=401)
    
    #Endpoint crear playlist
    #Si el método es post es una creación de una playlist
    if request.method == "POST":
        playlistName = request.POST.get("playlistName")

        if playlistName != "":

            queryPlaylists = Playlist.objects.filter(nombre=playlistName).count()
            if queryPlaylists > 0:
                return JsonResponse({"ALERTA":"YA EXISTE UNA PLAYLIST CON EL NOMBRE INTRODUCIDO"},status=409)
            else:
                newPlaylist = Playlist(nombre=playlistName)
                newPlaylist.save()
                return JsonResponse({"INFO":"SE HA CREADO SATISFACTORIAMENTE LA PLAYLIST"},status=201)
        else:
            return JsonResponse({"ALERTA":"EL NOMBRE DE LA PLAYLIST NO PUEDE QUEDAR VACIO"},status=400)
        
    #Endpoint listar playlists
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
        return JsonResponse({"ALERTA":"NO HAS MANDADO UN MÉTODO ADECUADO. PRUEBA CON POST O GET"})
        
@csrf_exempt
#funcion para eliminar plahylist
def eliminarPlaylist (request,playlistid):
#Guardar datos de token y comprobar que se esté pasando ese token
    #token = request.headers.get("sessionToken",None)

    #if token == None:
     #   return JsonResponse({"ALERTA":"NO SE HA PASADO UN TOKEN DE USUARIO"},status=401)
    
    #Endpoint borrar playlist por id
    #Comprobamos el método
    if request.method == "DELETE":

        checkidQuery = Playlist.objects.filter(id = playlistid).count()

        #COmprobamos que exista la playlist a borrar
        if checkidQuery == 0:
            return JsonResponse({"ERROR":"LA PLAYLIST CON EL ID SELECCIONADO NO EXISTE"},status=409)
        else:
            deleteQuery = Playlist.objects.filter(id = playlistid).delete()
            return JsonResponse({"INFO":"PLAYLIST ELIMINADA SATISFACTORIAMENTE"},status=200)
    
    #Endpoint buscar playlist por id para ver su contenido
    elif request.method == "GET":

        queryPlaylist = Canciones.select_related('playlist').filter(id = playlistid)