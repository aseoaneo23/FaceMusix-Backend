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
        return JsonResponse({"error":"no es un método POST"}, status=405)
    else:
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
#Función para el login y logout dependiendo del método.
def login_logout (request):
    if request.method == "POST":
        
    

