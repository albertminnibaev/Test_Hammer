import random
import time

from django.utils.crypto import get_random_string
from drf_yasg.openapi import Parameter, Schema, TYPE_OBJECT, TYPE_STRING, IN_FORM
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsProfileUser
from users.serializers import UserSerializer, UserUpdateSerializer, UserRetrieveSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileUser]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileUser]


class VerificationView(APIView):
    """
    Класс представления для отправки 4х значного кода подтверждения.
    """

    @swagger_auto_schema(request_body=Schema(
                             type=TYPE_OBJECT,
                             required=['phone'],
                             properties={
                                 'phone': Schema(type=TYPE_STRING)},
                             responses={201: 'slug not found'}))
    def post(self, request):
        """
        Метод POST для отправки кода подтверждения.
        Принимает номер телефона, проверяет наличие пользователя с этим номером.
        Если пользователь существует, генерирует 4-х значный код подтверждения (otp_code),
        сохраняет его для пользователя в базе данных и имитирует отправку кода авторизации.
        Если пользователь не существует, генерирует 4-х значный код подтверждения (otp_code),
        создает нового пользователя с указанным номером телефона и сохраняет его в базе данных.
        Возвращает ответ с сообщением об успешной отправке кода или создании кода.
        """
        phone_number = request.data.get('phone')
        user = User.objects.filter(phone=phone_number).first()
        print(user)

        if user is not None:
            otp_code = random.randint(1000, 9999)
            user.otp_code = str(otp_code)
            user.save()

            # Имитация отправки кода авторизации
            time.sleep(2)

            # Отправка кода авторизации на номер телефона пользователя через сервис SMS Aero
            # send_sms(phone_number, otp_code)

            print('otp_code:', otp_code)

            return Response({'message': 'Code sent successfully'})

        else:
            otp_code = random.randint(1000, 9999)

            user = User.objects.create(phone=phone_number, otp_code=str(otp_code))  # Сохранение профиля в БД

            # Имитация отправки кода авторизации
            time.sleep(2)

            # Отправка кода авторизации на номер телефона пользователя через сервис SMS Aero
            # send_sms(phone_number, otp_code)

            print('otp_code:', otp_code)

            return Response({'message': 'Code created successfully'})


class UserAuthenticationView(APIView):
    """
        Класс представления для аутентификации пользователя.
    """
    @swagger_auto_schema(request_body=Schema(
                             type=TYPE_OBJECT,
                             required=['phone', 'otp_code'],
                             properties={
                                 'phone': Schema(type=TYPE_STRING),
                                 'otp_code': Schema(type=TYPE_STRING)}))
    def post(self, request):
        """
        Метод POST для аутентификации пользователя.
        Принимает номер телефона и код подтверждения.
        Проверяет наличие пользователя с указанным номером телефона.
        Если пользователь существует и код подтверждения верный,
        генерирует токен доступа и возвращает его в ответе.
        Возвращает ответ с токеном доступа в случае успешной аутентификации,
        или ответ с сообщением об недопустимых учетных данных.
        """
        phone_number = request.data.get('phone')
        otp_code = request.data.get('otp_code')

        user = User.objects.filter(phone=phone_number).first()
        if not user or not user.check_otp_code(otp_code):
            return Response({'message': 'Invalid credentials'}, status=400)

        # генерация токена для доступа
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # генерация и сохранения реферрального кода пользователя
        user.referral_code = get_random_string(length=6)
        user.save()

        return Response({'access_token': access_token,
                         'refresh_token': str(refresh)})


class ReferralView(APIView):
    """
    Класс представления для ввода 6ти значного рефереального кода пользователя.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=Schema(
                             type=TYPE_OBJECT,
                             required=['referral_code'],
                             properties={
                                 'referral_code': Schema(type=TYPE_STRING)}))

    def post(self, request):
        """
        Метод POST для привязки пользователя к реферу.
        Принимает рефереальны код рефера.
        Проверяет наличие пользователя с указанным рефереальным код.
        Если пользователь существует, формирует связь между рефером и рефералом.
        """
        referral_code = request.data.get('referral_code')
        print(referral_code)

        user = User.objects.filter(referral_code=referral_code).first()

        if request.user.referral_code_refer:
            return Response({'message': 'You already have an activated referral code'}, status=400)

        if user is None:
            return Response({'message': 'Invalid credentials'}, status=400)

        else:
            request.user.referral_code_refer = referral_code
            request.user.refer = user
            request.user.save()

            return Response({'referral_code_refer': referral_code,
                             'refer': str(request.user.refer.id)})
