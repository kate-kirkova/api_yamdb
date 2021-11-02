import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # поле role сделвть read_only в сериализаторе
    bio: str = models.TextField('About user', blank=True, null=True)
    role: str = models.CharField(
        'User role', choices=['admin', 'moderator', 'user'])
    confirmation_code: str = models.CharField(
        max_length=12, default=uuid.uuid4)


class Review(models.Model):
    pass


class Title(models.Model):
    pass


class Comment(models.Model):
    pass


class Genre(models.Model):
    pass


class Category(models.Model):
    pass
