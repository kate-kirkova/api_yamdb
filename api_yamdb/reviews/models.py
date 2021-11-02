import uuid
from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


ROLES = (
    ('ADMIN', 'Admin'),
    ('MODERATOR', 'Moderator'),
    ('USER', 'User')
)


class User(AbstractUser):
    bio = models.TextField('About user', blank=True, null=True)
    role = models.CharField(
        'User role', choices=ROLES, default='User', max_length=10)
    confirmation_code: str = models.CharField(
        max_length=12, default=uuid.uuid4)


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='author')
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='reviews',
        verbose_name='title')
    rating = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(10)])


class Title(models.Model):
    name = models.CharField('Название', max_length=150,
                            blank=False, unique=True)
    year = models.PositiveIntegerField(
        'Год выхода', validators=[MaxValueValidator(dt.now().year)],
        blank=False,)
    description = models.TextField('Описание', blank=True)
    genre = models.ForeignKey('Genre', blank=False, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', blank=False, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    pass


class Genre(models.Model):
    pass


class Category(models.Model):
    pass
