from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.urls import reverse

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'email', 'role', 'first_name', 'last_name', 'phone_number')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name =validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role']
        )
        self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        token = user.username  # Dev only placeholder
        verification_link = f"http://localhost:8000/api/verify-email/{token}/"
        send_mail(
            'Verify your account',
            f'Click to verify: {verification_link}',
            'noreply@rivaanah.com',
            [user.email]
        )

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'address', 'role', 'gender', 'profile_picture', 'date_of_birth', 'phone_number']
        read_only_fields = ['id', 'username', 'role', 'email']
        