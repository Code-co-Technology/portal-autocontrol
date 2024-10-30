from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from utils.renderers import UserRenderers
from utils.permissions import IsLogin

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from car_app.models import CarBrand, CarModel, Cars
from car_app.car.serializers import CarBarndSerializer, CardModelSerializer, CarsSerializer, CarSerializer


class CardBrandView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=["Cars"],
        manual_parameters=[
            openapi.Parameter("name", openapi.IN_QUERY, description="Car brand name to search", type=openapi.TYPE_STRING),
        ],
        responses={200: CarBarndSerializer(many=True)}
    )
    def get(self, request):
        search_name = request.query_params.get("name", None)

        if search_name:
            objects = CarBrand.objects.filter(name__icontains=search_name).order_by("-id")
        else:
            objects = CarBrand.objects.all().order_by("-id")
        serializer = CarBarndSerializer(objects, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CardModelView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=["Cars"],
        manual_parameters=[
            openapi.Parameter("name", openapi.IN_QUERY, description="Car model name to search", type=openapi.TYPE_STRING),
        ],
        responses={200: CardModelSerializer(many=True)}
    )
    def get(self, request, id_brand):
        search_name = request.query_params.get("name", None)

        if search_name:
            objects = CarModel.objects.filter(brand=id_brand, name__icontains=search_name).order_by("-id")
        else:
            objects = CarModel.objects.filter(brand=id_brand).order_by("-id")
        serializer = CardModelSerializer(objects, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyCarsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=["Cars"],
        responses={200: CarsSerializer(many=True)}
    )
    def get(self, request):
        objects = Cars.objects.filter(owner=request.user).order_by("-id")
        serializer = CarsSerializer(objects, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Cars"],
        request_body=CarSerializer
    )
    def post(self, request):
        serializer = CarSerializer(data=request.data, context={"owner":request.user, "request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CarView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=["Cars"],
        responses={200: CarsSerializer(many=False)}
    )
    def get(self, request, pk):
        objects = get_object_or_404(Cars, id=pk)
        serializer = CarsSerializer(objects, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Cars"],
        request_body=CarSerializer,
    )
    def put(self, request, pk):
        instance = get_object_or_404(Cars, id=pk)
        serializer = CarSerializer(instance=instance, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=["Cars"],
        responses={204:  "No Content"}
    )
    def delete(self, request, pk):
        car_delete = get_object_or_404(Cars, id=pk)
        car_delete.delete()
        return Response({"message": "Машина удален"}, status=status.HTTP_204_NO_CONTENT)
