import uuid
from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

ROLES = (
    ('moderator', 'moderator'),
    ('user', 'user'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    bio = models.TextField('About user', blank=True, null=True)
    role = models.CharField(
        'User role', choices=ROLES, default='user', max_length=10)
    confirmation_code = models.CharField(
        max_length=36, default=uuid.uuid4)

    def __str__(self) -> str:
        return self.username


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=False)

    class Meta:
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=150, blank=False)
    year = models.PositiveIntegerField(
        'Год выхода', validators=[MaxValueValidator(dt.now().year)],
        blank=False,)
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, 'Genre', blank=False)
    category = models.ForeignKey(
        'Category', blank=False, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='author')
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='reviews',
        verbose_name='title')
    text = models.TextField('Комментарий к отзыву')
    score = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            ),
        ]


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


class Category(models.Model):
    name = models.CharField('Категория', max_length=256, unique=True)
    slug = models.SlugField(unique=True, blank=False, max_length=50)

    class Meta:
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name
