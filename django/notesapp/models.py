from datetime import datetime, timedelta
import re
from django.utils import timezone
from django.db.models.deletion import CASCADE
import jwt as jwt
from django.contrib.auth.models import AbstractUser
from django.db import models
from configs import settings


class User(AbstractUser):
    """
    [User]
    Model of User instance. Uses Django AbstractUser
    """
    username = models.CharField(max_length=50, unique=True, verbose_name='Username')

    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return f"{self.username}"

    @property
    def token(self) -> str:
        return self._generate_jwt_token()

    def _generate_jwt_token(self) -> str:
        """
        Generates user JWT token to authorize requests. Valid for 30 days
        """
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            'id': self.pk,
            'expire': str(dt)
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Note(models.Model):
    """
    [Note]
    Model of Note instance.
    """
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date created")

    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.title}"

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
