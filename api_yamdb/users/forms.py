from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import CustomUser


class UserForm(ModelForm):
    model = CustomUser

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if cleaned_data.get('username') == 'me':
            raise ValidationError('Имя пользователя "me" не разрешено.')
        return cleaned_data
