from rest_framework import serializers
from reviews.models import Category, Genre, MyOwnUser, Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyOwnUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ('name', 'slug')
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'rating')


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyOwnUser
        fields = ('email', 'username')


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    conf_code = serializers.CharField(max_length=150)
