from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Title(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Произведение')
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(timezone.now().year),
                    MinValueValidator(0)],
        verbose_name='Год создания'
    )
    description = models.CharField(max_length=255,
                                   blank=True,
                                   null=True,
                                   verbose_name='Описание'
                                   )
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Объект творчества'
        verbose_name_plural = 'Объекты творчества'

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Тип категории')
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(unique=True,
                            max_length=50,
                            verbose_name='Название жанра')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Название',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст обзора',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка зрителя',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария к отзыву'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий к обзору'
        verbose_name_plural = 'Комментарии к обзору'

    def __str__(self):
        return self.text
