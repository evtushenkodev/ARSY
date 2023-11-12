from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.exceptions import TokenError

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializer import RegisterSerializer, VerifySerializer, UserProfileSerializer, \
    PasswordChangeSerializer, LoginSerializer, PasswordResetOtpSerializer, PasswordResetEmailSerializer, EmptySerializer
from .services import RegisterService, VerifyService, LoginService, \
    PasswordChangeService, ResetPasswordEmailService, PasswordResetOtpService


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = RegisterService.create_user(serializer.validated_data)
        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)


class VerifyView(CreateAPIView):
    serializer_class = VerifySerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            message = VerifyService.verify_otp(email, otp)
            return Response(message, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user_data = LoginService.authenticate_user(email, password)

        if user_data is not None:
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'Неверный email или пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmptySerializer

    def post(self, request, **kwargs):
        refresh_token = request.data.get('refresh_token')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Вы успешно вышли из аккаунта"}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error": "Произошла ошибка при выходе из аккаунта, "
                                      "возможно, токен уже отозван или не существует"},
                            status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    @swagger_auto_schema(
        request_body=PasswordChangeSerializer,
        responses={200: 'Success', 400: 'Bad Request'}
    )
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        user = self.request.user

        try:
            PasswordChangeService.change_user_password(user, old_password, new_password)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Пароль успешно изменен.'}, status=status.HTTP_200_OK)


class PasswordResetEmailView(CreateAPIView):
    # для отправки кода на почту

    serializer_class = PasswordResetEmailSerializer

    def post(self, request, *args, **kwargs):
        reset_password_service = ResetPasswordEmailService()
        return reset_password_service.password_reset_email(self, request)


class PasswordResetOtpView(CreateAPIView):
    serializer_class = PasswordResetOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get("code")
            password = serializer.validated_data["password"]
            success, message, http_status = PasswordResetOtpService.password_reset_new_password(code, password)
            return Response(data={"detail": message}, status=http_status)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

