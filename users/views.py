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
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


# ajouter une tache par le chef 
@api_view(['POST'])
def chef_add_tache(request):
    chef_id = request.data.get('chef_id')
    employes_id = request.data.get('employes_id', [])
    description = request.data.get('description')
    etat = request.data.get('etat')
    importance = request.data.get('importance')
    print("chef_id",chef_id)
    print("employes_id",employes_id)
    print("description",description)
    # print("etat",etat)
    print("importance",importance)
    # Vérifier si tous les champs requis sont présents dans la requête
    if not (chef_id and description and etat and importance):
        print('da5lt lhadi')
        return Response({"error": "Veuillez fournir chef_id, description, etat et importance."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Récupérer le chef associé à l'identifiant fourni
    chef = get_object_or_404(Chef, id=chef_id)
    print('cheef 2 ',chef)
    print(':: ',chef)
    tache = Tache.objects.create(
                chef=chef,
                description=description,
                etat=etat,
                importance=importance
            )
    print('sss',tache)
    
    # Récupérer la liste des employés associés aux identifiants fournis
    # for emp_id in employes_id:
    #     employe = get_object_or_404(Employe, id=emp_id)
    #     tache.employes.add(employe)
    #     print('TacheSerializer(tache).data ::',TacheSerializer(tache).data)
    response_data = {
            'message': 'Tâche créée avec succès.',
            'data': TacheSerializer(tache).data
        }
    return Response(response_data, status=status.HTTP_201_CREATED)

  



# modifier un tache par le chef



# Associate tasks automatically with employees based on their roles

