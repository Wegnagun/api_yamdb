from django.forms import ValidationError
from requests import request
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Genre, MyOwnUser, Title, Comment, Review


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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, many=False)
    review = serializers.StringRelatedField(
        read_only=True, many=False)

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, many=False)
    title = serializers.StringRelatedField(
        read_only=True, many=False)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if not Review.objects.filter(
            title=get_object_or_404(
                Title, pk=self.context['view'].kwargs.get('title_id')),
                author=request.user).exists():
            return data
        raise ValidationError(
            'На одно произведение пользователь'
            'может оставить только один отзыв.')
