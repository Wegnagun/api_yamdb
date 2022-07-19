from django.contrib.admin import ModelAdmin, register

from .models import CustomUser


@register(CustomUser)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'role')
    fields = ('username', 'first_name', 'last_name',
              'email', 'role', 'bio')
