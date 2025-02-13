from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(write_only=True, help_text='Phone number or email')
    password = PasswordField(write_only=True)
    is_partner = serializers.BooleanField(write_only=True, default=False, required=False)
    refresh = serializers.CharField(read_only=True, min_length=200, max_length=300)
    access = serializers.CharField(read_only=True, min_length=200, max_length=300)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        is_partner = attrs.get('is_partner')

        if '@' in login:
            user = authenticate(email=login, password=password)
        else:
            user = User.objects.filter(phone_number=login).first()
            user = authenticate(email=user.email if user else None, password=password)

        if not user:
            raise AuthenticationFailed(detail='Invalid login or password')

        if is_partner and not user.is_partner:
            raise AuthenticationFailed(detail='User is not a partner')

        if not user.is_active:
            raise AuthenticationFailed(detail='User account is disabled')

        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data

    def create(self, validated_data):
        return validated_data

    @staticmethod
    def get_token(user) -> RefreshToken:
        return RefreshToken.for_user(user)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], min_length=8)
    full_name = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'email', 'password', 'full_name', 'phone_number',
        )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            full_name=validated_data.get('full_name'),
            phone_number=validated_data.get('phone_number'),
        )
        user.set_password(validated_data['password'])
        user.save()
        refresh: RefreshToken = RefreshToken.for_user(user)
        user.refresh = str(refresh)
        user.access = str(refresh.access_token)
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['refresh'] = instance.refresh
        ret['access'] = instance.access
        return ret


class UserSerializer(serializers.ModelSerializer):
    is_partner = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'inn', 'is_partner', 'date_joined']
