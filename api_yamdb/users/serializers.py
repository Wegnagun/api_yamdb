from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and (request.method != 'PATCH' or request.user.is_admin):
            fields['role'].read_only = False
        return fields
