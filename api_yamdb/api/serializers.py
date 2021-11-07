from rest_framework import serializers, status
from rest_framework.response import Response
from reviews.models import Category, Genre, Title, User


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        '''Checks if the email is already in the database'''
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError('This email address is already in use')
        return lower_email
    
    def validate_username(self, value):
        ''' Assures that username is not equal to 'me' '''
        lower_username = value.lower()
        if lower_username == 'me':
            raise serializers.ValidationError('Please use a different username')
        return lower_username


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        return user

    class Meta:
        model = User
        fields = ('email', 'username')


class GetJWTTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate_username(self, value):
        # необходимо вернуть 404 статус если юзера не существует
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError(detail='Username not found')

    def validate_confirmation_code(self, value):
        if not User.objects.filter(confirmation_code=value).exists():
            raise serializers.ValidationError('Invalid code')

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )
