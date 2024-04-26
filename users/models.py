from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from enum import Enum  # Importez Enum du module enum
from django.core.validators import MinValueValidator, MaxValueValidator


def upload_path_profile_pic(instance, filename):
    return 'coversProfile_pic/{0}/{1}'.format(instance.username, filename)

def upload_path_post_pic(instance, filename):
    return 'covers_post_pic/{0}/{1}'.format(instance.user.username, filename)


choices={'employee':'employee','chef':'chef'}


class User(AbstractUser):
  username=models.CharField( max_length=50,unique=True)
  email=models.EmailField(unique=True)
  profile_pic = models.ImageField(upload_to=upload_path_profile_pic,default='aaa.jpg')
  role = models.CharField(max_length=10, choices=choices, default=choices.get('employee'))
  USERNAME_FIELD='email'
  REQUIRED_FIELDS=['username']
  def __str__(self):
        return self.username

class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE )
    def __str__(self):
        return self.user.username
    

ETAT_CHOICES = (
    ('ready', 'ready'),
    ('en_cours_execution', 'en_cours_execution'),
    ('finish', 'finish'),
    ('probleme', 'probleme'),
)

IMPORTANCE_CHOICES = (
    ('urgence', 'urgence'),
    ('not_urgence', 'not_urgence'),
    ('moderate', 'moderate'),
)

class Tache(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, related_name='tasks')
    employes = models.ManyToManyField(Employe, verbose_name="Employés associés", related_name='tasks')
    description = models.TextField()
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='ready')
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='not_urgence')
    def __str__(self):
        return f"Tâche-{self.importance}-{self.description[:20]}"
    class Meta:
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"