from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from api_yamdb.settings import EMPTY_STRING_FOR_ADMIN_PY

from .models import Categories, Genres, Titles, MyOwnUser

ModelAdmin.empty_value_display = EMPTY_STRING_FOR_ADMIN_PY


class MyUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'role')
    fields = ('username', 'first_name', 'last_name', 'email', 'role',
              'biography')


admin.site.register(MyOwnUser, MyUserAdmin)


@register(Titles)
class TitlesAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'category',
                    'creation_year', 'description', 'get_genres')
    search_fields = ('name',)
    list_filter = ('name',)

    def get_genres(self, obj):
        return '\n, '.join([str(genre) for genre in obj.genre.all()])


@register(Categories)
class CategoriesAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)


@register(Genres)
class GenresAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
