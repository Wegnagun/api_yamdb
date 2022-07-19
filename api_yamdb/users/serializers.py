from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

        def validate_username(self, value):
            if value == 'me':
                raise serializers.ValidationError('Меня не ложно быть - me.')
            return value
