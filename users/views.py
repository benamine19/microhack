from django.shortcuts import render
from users.serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from AI.VoiceToTask import VoiceToTask
# Create your views here.


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializerChef

# il faut que l'utilsateur soit le chef pour etre valaible d'ajouter des employer
@api_view(['POST'])
def chef_add_employe(request):
    chef_id = request.data.get('chef_id')
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    profile_pic = request.data.get('profile_pic')
    if not (username and password and email):
        return Response({"error": "Please provide username, password, and email for the new employee."},
                        status=status.HTTP_400_BAD_REQUEST)
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username is already taken. Please choose a different username."},
                        status=status.HTTP_400_BAD_REQUEST)
    chef=get_object_or_404(Chef,id=chef_id)
    user=User.objects.create(username=username,email=email,profile_pic=profile_pic,role='employee')
    user.set_password(password)
    user.save()
    employe=Employe.objects.create(
            user=user,
            chef=chef,
    )
    response="Succed to create employee"
    return Response({
            'response':response,
            'data 1':UserSerializer(user).data
            } ,status=status.HTTP_200_OK)


# ajouter une tache par le chef 
@api_view(['POST'])
def chef_add_tache_form(request):
    chef_id = request.data.get('chef_id')
    description = request.data.get('description')
    etat = request.data.get('etat')
    importance = request.data.get('importance')

    # Vérifier si tous les champs requis sont présents dans la requête
    if not (chef_id and description and etat and importance):
        print('da5lt lhadi')
        return Response({"error": "Veuillez fournir chef_id, description, etat et importance."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Récupérer le chef associé à l'identifiant fourni
    chef = get_object_or_404(Chef, id=chef_id)

    tache = Tache.objects.create(
                chef=chef,
                description=description,
                etat=etat,
                importance=importance
            ) 
    response_data = {
            'message': 'Tâche créée avec succès.',
            'data': TacheSerializer(tache).data
        }
    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def chef_add_tache_audio(request):
    chef_id = request.data.get('chef_id')
    audio = request.FILES.get('audio')
    #return Response( status=status.HTTP_201_CREATED)
    # Vérifier si tous les champs requis sont présents dans la requête
    if not (chef_id and audio):
        return Response({"error": "Veuillez fournir chef_id, description, etat et importance."},
                        status=status.HTTP_400_BAD_REQUEST)   
         
    file_name = 'TaskAudio.m4a'  # Example: You may use a unique file name based on time or user ID
        
    # Specify the path where you want to save the audio file
    save_path = 'Audio/' + file_name


    # Save the audio data to a file
    with open(save_path, 'wb') as destination:
        for chunk in audio.chunks():
            destination.write(chunk)
    
    Task = VoiceToTask(save_path)
    Task
    print(Task)
    # Récupérer le chef associé à l'identifiant fourni
    chef = get_object_or_404(Chef, id=chef_id)

    #get the list of employes called by the manager
    employes = []
    

        
    
    tache = Tache.objects.create(
                chef=chef,
                importance = Task["Importance"],
                description=Task["Task"],
                duration = Task["Duration"],
            ) 
    
    for name in Task["Names"]:
        name = name.lower()
        user = User.objects.filter(Q(username__icontains=name) ).distinct().first()
        print("brqqq /",user)
        
        if(user[0]):
            print("sdfsdf /",user)
            emp = get_object_or_404(user=user[0])
            tache.employes.add(emp)
            tache.save()
    
    
    response_data = {
            'message': 'Tâche créée avec succès.',
            'data': TacheSerializer(tache).data
        }
    return Response(response_data, status=status.HTTP_201_CREATED)



# modifier un tache par le chef



# Associate tasks manually to employes 
@api_view(['POST'])
def associate_tasks_to_employes_manually(request):
    employes_id = request.data.get('employes_id', [])
    tache_id = request.data.get('tache_id')
    # Vérifier si tous les champs requis sont présents dans la requête
    if not (employes_id and tache_id):
        return Response({"error": "Veuillez fournir employes_id et tache_id."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Récupérer la tâche associée à l'identifiant fourni
    tache = get_object_or_404(Tache, id=tache_id)

    # Récupérer la liste des employés associés aux identifiants fournis
    for emp_id in employes_id:
        employe = get_object_or_404(Employe, id=emp_id)
        tache.employes.add(employe)

    response_data = {
        'message': 'Tâche associée aux employés avec succès.',
        'data': TacheSerializer(tache).data
    }
    return Response(response_data, status=status.HTTP_200_OK)

