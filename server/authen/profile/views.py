from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from utils.renderers import UserRenderers
from utils.permissions import IsLogin

from authen.models import CustomUser
from authen.profile.serializers import UserProfileSerializer, UserProfileUpdateSerializer


class UserProfileView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=["Auth"], responses={200: UserProfileSerializer(many=True)})
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Auth"], request_body=UserProfileUpdateSerializer)
    def put(self, request):
        queryset = get_object_or_404(CustomUser, id=request.user.id)
        serializer = UserProfileUpdateSerializer(context={"request": request}, instance=queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Auth"], responses={204:  'No Content'})
    def delete(self, request):
        user_delete = CustomUser.objects.get(id=request.user.id)
        user_delete.delete()
        return Response({"message": "delete success"}, status=status.HTTP_204_NO_CONTENT)