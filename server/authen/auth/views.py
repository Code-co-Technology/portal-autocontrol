from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema

from utils.renderers import UserRenderers
from authen.auth.serializers import UserRegisterSerializer, UserLoginSerializer


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserRegisterView(APIView):
    render_classes = [UserRenderers]

    @swagger_auto_schema(tags=['Auth'], request_body=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instanse = serializer.save()
            tokens = get_token_for_user(instanse)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    render_classes = [UserRenderers]

    @swagger_auto_schema(tags=["Auth"], request_body=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                tokens = get_token_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Этот пользователь недоступен для системы"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)