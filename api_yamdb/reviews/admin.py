from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from api_yamdb.settings import EMPTY_STRING_FOR_ADMIN_PY

from .models import Category, Genre, MyOwnUser, Title, Review, Comment

ModelAdmin.empty_value_display = EMPTY_STRING_FOR_ADMIN_PY


class MyUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'role')
    fields = ('username', 'first_name', 'last_name', 'email', 'role',
              'bio')


admin.site.register(MyOwnUser, MyUserAdmin)
admin.site.register(Review)
admin.site.register(Comment)


@register(Title)
class TitlesAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'category',
                    'year', 'description', 'get_genres')
    search_fields = ('name',)
    list_filter = ('name',)

    def get_genres(self, obj):
        return '\n, '.join([str(genre) for genre in obj.genre.all()])


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
