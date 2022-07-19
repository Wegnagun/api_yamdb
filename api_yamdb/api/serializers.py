from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Genre, MyOwnUser, Title, Comment, Review


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MyOwnUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

        def validate_username(self, value):
            if value == 'me':
                raise serializers.ValidationError(
                    'Имя пользователя "me" не разрешено.'
                )
            return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyOwnUser
        fields = ('email', 'username')


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    conf_code = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = MyOwnUser
        fields = ('username', 'conf_code')


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

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10.'
            )
        return value


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyOwnUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
