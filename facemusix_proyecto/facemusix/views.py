from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

from .models import Amigos,Canciones,Cancionplaylist,Playlist,Usuarios,lbumes,Ratings

@csrf_exempt
#Función para el registro de usuarios
def Registro (request):
    #Si la petición no es POST mandar error, sólo puede ser un POST.
    if request.method != "POST":
        return JsonResponse({"error":"método HTTP no soportado"}, status=405)
    else:
        #Comprobamos que se pasen los campos todos cubiertos y las contraseñas coincidan
        if request.POST.get("name") == None or request.POST.get("username") == None or request.POST.get("email") == None or request.POST.get("password") == None or request.POST.get("confirmpassword") == None:
            return JsonResponse({"ALERTA":"DEBES CUBRIR TODOS LOS CAMPOS"},status=400)
        elif request.POST.get("password") != request.POST.get("confirmpassword"):
            return JsonResponse({"ALERTA":"LAS CONTRASEÑAS NO COINCIDEN"},status=400)
            
        #Se comprueba que no existe ningún usuario con ese email o usuario
        
        username = request.POST.get("username")
        email = request.POST.get("email")
        #Consultas para comprobar si existe el usuario
        queryEmails = Usuarios.objects.filter(email=email).count()
        queryUsernames = Usuarios.objects.filter(nombre_usuario=username).count()
        #Comprobaciones para evitar redundancia
        if(queryEmails > 0):
            return JsonResponse({"Mensaje":"el email ya esta registrado"})
        elif(queryUsernames > 0):
            return JsonResponse({"Mensaje":"el nombre de usuario ya esta en uso"})
        else:
            name = request.POST.get("name")
            password_withouthash = request.POST.get("password")
            password = make_password(password_withouthash)
        #Inserciones de los datos de usuario nuevos
            usuario = Usuarios(nombre=name,nombre_usuario=username,email=email,passwd=password)
            usuario.save()
            return JsonResponse({"Mensaje":"Registro exitoso"},status=201)
        

@csrf_exempt
#Función para el listado de playlists.
def playlists(request):
    #Guardar datos de token y comprobar que se esté pasando ese token
    token = request.headers.get("sessionToken",None)

    if token == None:
        return JsonResponse({"ALERTA":"NO SE HA PASADO UN TOKEN DE USUARIO"})
    #Si el método es post es una creación de una playlist
    elif request.method == "POST":
        playlistName = request.POST.get("playlistName")
        queryPlaylists = Playlist.objects.filter(nombre = playlistName).count()

        if queryPlaylists > 0:
            return JsonResponse({"ALERTA":"YA EXISTE UNA PLAYLIST CON EL NOMBRE INTRODUCIDO"})
        else:
            

