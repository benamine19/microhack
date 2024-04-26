from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns =[
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),    
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('RegisterViewChef/', RegisterView.as_view(), name='RegisterView'),
    path('chef_add_employe/', chef_add_employe, name='chef_add_employe'),
    path('chef_add_tache/', chef_add_tache, name='chef_add_tache'),
    path('chef_modifier_tache/', chef_modifier_tache, name='chef_modifier_tache'),
    path('chef_add_employes_to_tache/', chef_add_employes_to_tache, name='chef_add_employes_to_tache'),
    path('get_all_taches/', get_all_taches, name='get_all_taches'),
    path('get_all_employes/', get_all_employes, name='get_all_employes'),    
]