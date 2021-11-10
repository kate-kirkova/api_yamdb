import uuid
from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

ROLES = (
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
)


class User(AbstractUser):
    bio = models.TextField('About user', blank=True)
    role = models.CharField(
        'User role', choices=ROLES, default='user', max_length=10)
    confirmation_code = models.CharField(
        max_length=36, default=uuid.uuid4)

    def __str__(self) -> str:
        return self.username


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
    name = models.CharField('Название', max_length=150, blank=False)
    year = models.PositiveIntegerField(
        'Год выхода', validators=[MaxValueValidator(dt.now().year)],
        blank=False,)
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        'Genre', blank=False)
    category = models.ForeignKey(
        'Category', blank=False, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Отзыв о произведении')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:30]


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=False)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField('Категория', max_length=256, unique=True)
    slug = models.SlugField(unique=True, blank=False, max_length=50)

    def __str__(self) -> str:
        return self.name


# class GenreTitle(models.Model):
#     genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
#     title = models.ForeignKey(Title, on_delete=models.CASCADE)
