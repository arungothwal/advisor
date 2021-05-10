from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin
from django.contrib.sessions.models import Session
import jwt
from django.conf import settings
from rest_framework_jwt.utils import jwt_payload_handler
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('user must have an email')
        if not password:
            raise ValueError('user must have an password')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(max_length=40, unique=True)
    name = models.CharField(max_length=30,blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_jwt(self):
        """Function for creating JWT for Authentication Purpose"""
        payload = jwt_payload_handler(self)
        token = jwt.encode(payload, settings.SECRET_KEY)
        auth_token = token.decode('unicode_escape')
        return auth_token

    def remove_all_sessions(self):

        user_sessions = []
        all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in Session.objects.all():
            if str(self.pk) == session.get_decoded().get('_auth_user_id'):
                user_sessions.append(session.pk)
        return Session.objects.filter(pk__in=user_sessions).delete()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')


class Advisor(models.Model):
    name = models.CharField(max_length=20,blank=True,null=True)
    pic = models.ImageField(upload_to="advisor/images",default='')

    def __str__(self):
        return str(self.id)
