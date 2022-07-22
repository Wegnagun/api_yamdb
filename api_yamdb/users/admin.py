from django.contrib.admin import ModelAdmin, register
from django.contrib.auth import get_user_model


user = get_user_model()


@register(user)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'role')
    fields = ('username', 'first_name', 'last_name',
              'email', 'role', 'bio')
