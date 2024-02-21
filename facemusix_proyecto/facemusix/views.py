from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from .models import Amigos, Canciones, Cancionplaylist, Playlist, Usuarios, Ratings
from django.core.paginator import Paginator

# Comprobaciones de JWT
SECRET_KEY = 'clavesegura' #clave almacenada de prueba 
@csrf_exempt
def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

@csrf_exempt
def verify_token(request):
    token = request.META.get('HTTP_AUTHORIZATION',None)
    if not token:
        return JsonResponse({"Message": "Token is missing"}, status=401),None,None
    
    try:
        if token.startswith('Bearer '):
            token = token.split(' ')[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return None, payload,token
    except jwt.ExpiredSignatureError:
        return JsonResponse({"Error":"Token has expired"}, status=401),None,None
    except jwt.InvalidTokenError:
        return JsonResponse({"Error":"Token inválido"},status=401),None,None
    
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

        try:
            email = json_respuesta["email"]
            password = json_respuesta["password"]
        except KeyError:
            return JsonResponse({"error": "Faltan parámetros"}, status=404)

        if email == "" or password == "":
            return JsonResponse({"error": "Los campos no pueden estar vacíos."}, status=400)
        else:
            queryEmail = Usuarios.objects.filter(email=email).count()
            
            if queryEmail == 0:
                return JsonResponse({"error": "Email incorrecto."}, status=405)
            elif check_password(password, Usuarios.objects.get(email=email).passwd) == 0:
                return JsonResponse({"error": "Contraseña incorrecta."}, status=405)
            else:

                token = create_token(Usuarios.objects.get(email=email).id)

                Usuarios.objects.filter(email=email).update(token=token)
                return JsonResponse({"token": token}, status=201)
            
    elif request.method == "PATCH":

        error_response,payload,token= verify_token(request)

        if error_response:
            return error_response
        else:
            Usuarios.objects.filter(token=token).update(token=None)
            return JsonResponse({"status": "logout successfully"})
    else:
        return JsonResponse({"error": "No se ha pasado un DELETE o POST"})


@csrf_exempt
# Función para el listado o creación de playlists.
def Playlists(request):

    #Guardar datos de token y comprobar que se esté pasando ese token
    error_response,payload,token= verify_token(request)

    #Endpoint crear playlist
    #Si el método es post es una creación de una playlist
    if error_response:
        return error_response
    else:
        if request.method == "POST":
            playlistName = request.POST.get("playlistName")

            if playlistName != "":

                queryPlaylists = Playlist.objects.filter(nombre=playlistName).count()
                if queryPlaylists > 0:
                    return JsonResponse({"ALERTA":"YA EXISTE UNA PLAYLIST CON EL NOMBRE INTRODUCIDO"},status=409)
                else:
                    Playlist(nombre=playlistName).save()
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
def playlistById (request,playlistid):
#Guardar datos de token y comprobar que se esté pasando ese token
    error_response,payload,token= verify_token(request)

    if error_response:
        return error_response
    else:
    #Endpoint borrar playlist por id
    #Comprobamos el método
        if request.method == "DELETE":

            checkidQuery = Playlist.objects.filter(id = playlistid).count()

            #COmprobamos que exista la playlist a borrar
            if checkidQuery == 0:
                return JsonResponse({"ERROR":"LA PLAYLIST CON EL ID SELECCIONADO NO EXISTE"},status=409)
            else:
                Playlist.objects.filter(id = playlistid).delete()
                return JsonResponse({"INFO":"PLAYLIST ELIMINADA SATISFACTORIAMENTE"},status=200)
        
        #Endpoint buscar playlist por id para ver su contenido
        elif request.method == "GET":
            #Query que devuelve un array de objetos que son canciones con sus campos. Si un campo de ellas es foreign,
            #también será un objeto. 
            queryPlaylist = Cancionplaylist.objects.filter(playlist = playlistid).select_related('cancion')
            
            if queryPlaylist.count() < 1:
                return JsonResponse({"INFO":"La playlist con id seleccionado no existe, prueba con otro id"},status=400)
                
            songs_list = []
            #Recorremos el array y guardamos en un diccionario los datos de las canciones que queremos y en un array a su vez
            for cancion in queryPlaylist:
                song = {
                    'nombre': cancion.cancion.título,
                    'duración': cancion.cancion.duración,
                    'album': cancion.cancion.album.título,#* --> aquí queremos el titulo del album y album es foreign en canciones.
                    'artista': cancion.cancion.artista.nombre
                }
                songs_list.append(song)

            return JsonResponse(songs_list, safe=False)

@csrf_exempt
#Función para buscar usuarios por id o por nombre
def buscarUsuarios (request):
    if request.method == "GET":

        error_response,payload,token= verify_token(request)

        if error_response:
            return error_response
        
        clientQuery = request.GET.get("search", None)

        if clientQuery is None or clientQuery == "":
            return JsonResponse({"ERROR":"No has pasado ningún parámetro \"search\" de búsqueda"}, status=400)
        if error_response:
            return error_response
        else:
            #Busqueda de el usuario solicitado por el search con conatins para que muestre todo lo que contenga esa cadena
            queryToSearch = Usuarios.objects.filter(nombre_usuario__icontains = clientQuery)

            #Ordenación
            sort_by = request.GET.get('sort', 'nombre_usuario')
            queryToSearch = queryToSearch.order_by(sort_by)

            #Paginación
            paginator = Paginator(queryToSearch, request.GET.get("limit",10))
            #Controlamos los resultados obtenidos
            if queryToSearch.exists():
                
                #Usamos la paginación
                page = request.GET.get('page',1)
                users = paginator.get_page(page)
                users__data=[]
                for user in users:
                    #Consulta de comprobación de tabla amigos, para ver si es o no mi amigo y cubrir el campo booleano following.

                    queryFollowing = Amigos.objects.filter(id_usuario = payload["user_id"], id_usuario_amigo = user.pk).count()
                    if queryFollowing < 1:
                        following = False
                    else:
                        following = True

                    #Instanciamos el objeto a mostrar
                    userDicc ={
                        "IMG": user.url_avatar,
                        "NAME": user.nombre,
                        "YOUFOLLOWHIM": following
                    }
                    users__data.append(userDicc)
                            
                return JsonResponse({"Usuarios" : users__data, "Total elements": paginator.count, "Page":page},status=200, safe=False)
            else:
                return JsonResponse({"INFO":"El usuario con nombre: " + clientQuery + " no existe."})
    else:
        return JsonResponse({"ERROR":"Metodo HTTP no soportado, prueba con un GET"},status=400)

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

def follow_unfollow(request):

    error_response,payload,token= verify_token(request)
    
    if error_response:
      return error_response
    
    # Comprobamos si el método es DELETE o POST
    
    if request.method == "DELETE":

        json_respuesta = json.loads(request.body)
        
        # Try para comprobar los parámetros enviados  en el header
        try:
            usuario = json_respuesta["usuario"]
            amigo = json_respuesta["amigo"]
        except KeyError: 
            return JsonResponse({"error": "Faltan parámetros"}, status=404) 
            # Si no existe algún parámetro, devuelve status 404
            
        # Try para comprobar si existe la relación, es decir, si el usuario sigue a el otro usuario
        try:
          # Query del modelo Amigos seleccionando el ID del usuario y del amigo al que sigue
            filtrado_usuarios_amigos = Amigos.objects.select_related("id_usuario").filter(id_usuario=usuario).get(id_usuario_amigo=amigo)
        except Amigos.DoesNotExist:
            return JsonResponse({"error": "Bad request"}, status=404)
            # Si no existe la relación, se lanza status 404. No se puede dejar de seguir si no existe.
            
        data = {
            "message": "El usuario "+filtrado_usuarios_amigos.id_usuario.nombre+" ha dejado de seguir a el usuario "+filtrado_usuarios_amigos.id_usuario_amigo.nombre
        }
        
        filtrado_usuarios_amigos.delete() # Se lanza el borrado de la fila del Query anterior.
        
        return JsonResponse(data)
      
    elif request.method == "POST":

        json_respuesta = json.loads(request.body)
        
        # Se comprueban los parámetros header en el POST.
        try:
            usuario = json_respuesta["usuario"]
            amigo = json_respuesta["amigo"]
        except KeyError:
            return JsonResponse({"error": "Faltan parámetros"}, status=404)
            # También se lanza un status 404 si no se encuentran los parámetros.

        try:
            # Misma QUERY que en el DELETE para encontrar la fila en el modelo Amigos con id usuario y amigo.
            filtrado_usuarios_amigos = Amigos.objects.select_related("id_usuario").filter(id_usuario=usuario).get(id_usuario_amigo=amigo)
            # En este caso, si se encuentra quiere decir que el usuario ya está siguiendo a el otros usuario.
            if filtrado_usuarios_amigos != None: #SI no devuelve ningún objeto usuario es que no hay la relacion de amigos entre los dos usuarios
                return JsonResponse({"error": "Ya estás siguiendo a este usuario"}, status=400)
                # Se devuelve un status 404, ya que no sepuede seguir si ya se sigue.
        
        # En la excepción es donde cambiamos la tabla, ya que es donde no existe la fila.
        except Amigos.DoesNotExist: 
            
            # Query para comprobar si existen usuarios con sus respectivos ids
            comprobacion_usuario = Usuarios.objects.filter(id=usuario).count()
            comprobacion_amigo = Usuarios.objects.filter(id=amigo).count()
            # Si no existes se lanza un error
            if comprobacion_amigo < 1 or comprobacion_usuario < 1:
                return JsonResponse({"error": "No existe ningún usuario o amigo con ese id"}, status=400)

            Amigos(id_usuario = Usuarios.objects.filter(id=usuario)[0], id_usuario_amigo=Usuarios.objects.filter(id=amigo)[0]).save() # Se lanza un QUERY para crear la relación.
            
            # Se devuelve un JSON para confirmar a quién se ha comenzado a seguir.
            return JsonResponse({"message": "Has comenzado a seguir a un nuevo usuario" })

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

