from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns =[
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),    
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('RegisterViewChef/', RegisterView.as_view(), name='RegisterView'),
    path('chef_add_employe/', chef_add_employe, name='chef_add_employe'),
    path('chef_add_tache_form/', chef_add_tache_form, name='chef_add_tache_form'),
    path('chef_add_tache_audio/', chef_add_tache_audio, name='chef_add_tache_audio'),
    path('associate_tasks_to_employes_manually/', associate_tasks_to_employes_manually, name='associate_tasks_to_employes_manually'),
    

]