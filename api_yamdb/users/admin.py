from django.contrib.admin import ModelAdmin, register
from django.contrib.auth import get_user_model

from .forms import UserForm


user = get_user_model()


@register(user)
class UserAdmin(ModelAdmin):
    form = UserForm
    list_display = ('username', 'email', 'role')
    fields = ('username', 'first_name', 'last_name',
              'email', 'role', 'bio')
