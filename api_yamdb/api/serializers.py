from rest_framework import serializers
from reviews.models import Categories, Genres, Titles, MyOwnUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyOwnUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'biography', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'rating')
