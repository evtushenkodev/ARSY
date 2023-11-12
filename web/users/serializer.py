from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User, PasswordResetOtp


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(max_length=40)
    name = serializers.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=40)
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "password"]


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']
        read_only_fields = ['email']


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]  # Валидатор на силу пароля
    )
    new_password2 = serializers.CharField(required=True)  # Второе поле пароля

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "The two password fields didn’t match."})
        return attrs

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2')


class PasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=40)

    class Meta:
        model = User
        fields = ['email']


class PasswordResetOtpSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, help_text="min length 8", min_length=8, write_only=True
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, help_text="Confirm password", min_length=8, write_only=True
    )

    class Meta:
        model = PasswordResetOtp
        fields = ["code", "password", "password2"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def update(self, instance, validated_data):
        user = instance.user
        user.set_password(validated_data['password'])
        user.save()

        instance.delete()

        return user


class EmptySerializer(serializers.Serializer):
    pass
