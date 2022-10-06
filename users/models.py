from django.db import models
from django.contrib.auth.models import AbstractUser

class token(model.Model):
    user=models.ForeignKey(user,verbose_name=_("token_use"), on_delete=models.CASCADE)
    user_token=models.CharField(_("tokens"), max_length=50)
class Permission(models.Model):
    name = models.CharField(max_length=200)

class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)

class User(AbstractUser):
    first_name=models.Charfield(max_lenght=10)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    username = None

    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.user
