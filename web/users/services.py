from django.contrib.auth import authenticate, hashers
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import status, response, serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .emails import send_email_confirmation, send_email_reset_password
from .models import User, PasswordResetOtp
from .utils import generate_random_code


class RegisterService:
    @staticmethod
    def create_user(user_data):
        try:
            user = User(
                email=user_data['email'],
                name=user_data['name'],
            )
            user.set_password(user_data['password'])
            user.save()
        except IntegrityError:
            raise serializers.ValidationError("A user with that email already exists.")

        send_email_confirmation(user.email)
        return user


class VerifyService:
    @staticmethod
    def verify_otp(email, otp):
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({'error': 'Неверный email.'})

        if user.otp != otp:
            raise ValidationError({'error': 'Неверный код подтверждения.'})

        user.is_active = True
        user.save()

        return {'message': 'Аккаунт успешно подтвержден.'}


class LoginService:
    @staticmethod
    def authenticate_user(email, password):
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return {
                'message': "Аутентификация прошла успешно",
                'status': status.HTTP_200_OK,
                'name': user.name,
                'email': user.email,
                "refresh_token": str(refresh),
                "access_token": str(access)
            }
        else:
            return None


class PasswordChangeService:
    @staticmethod
    def change_user_password(user, old_password, new_password):
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'Старый пароль указан неверно.'}, code=400)
        if old_password == new_password:
            raise ValidationError({'new_password': 'Новый пароль не должен совпадать со старым паролем.'}, code=400)
        user.set_password(new_password)
        user.save()
        return user


class ResetPasswordEmailService:
    @staticmethod
    def password_reset_email(view, request):
        serializer = view.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return response.Response(
                data={
                    "error": "Пользователь с указанным адресом электронной почты не найден."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        time = timezone.now() + timezone.timedelta(minutes=5)
        otp = generate_random_code()  # Генерируем случайный код

        password_reset_otp = PasswordResetOtp(
            user=user, code=otp, time=time
        )
        password_reset_otp.save()

        send_email_reset_password(user.email, otp)

        return response.Response(data={"detail": 'code send to your email'}, status=status.HTTP_200_OK)


class PasswordResetOtpService:
    @staticmethod
    def password_reset_new_password(code, password):
        try:
            password_reset_token = PasswordResetOtp.objects.get(
                code=code, time__gt=timezone.now()
            )
        except PasswordResetOtp.DoesNotExist:
            return False, "Invalid password reset code or the code has expired.", status.HTTP_400_BAD_REQUEST

        user = password_reset_token.user

        if user.check_password(password):
            return False, "New password cannot be the same as the current one.", status.HTTP_400_BAD_REQUEST

        user.password = hashers.make_password(password)
        user.save()

        password_reset_token.delete()
        return True, "Password successfully reset.", status.HTTP_200_OK
