from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from .models import Category, Genre, Title, Review, Comment


admin.site.register(Review)
admin.site.register(Comment)


@register(Title)
class TitlesAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'category',
                    'year', 'description', 'get_genres')
    search_fields = ('name',)
    list_filter = ('name',)

    def get_genres(self, title):
        return '\n'.join([genre.name for genre in title.genre.all()])


@register(Category)
class CategoriesAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)


@register(Genre)
class GenresAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
