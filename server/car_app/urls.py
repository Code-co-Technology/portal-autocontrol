from django.urls import path
from car_app.car.views import CardBrandView, CardModelView, MyCarsView, CarView


urlpatterns = [
    path('cars/brand/', CardBrandView.as_view()),
    path('cars/model/<int:id_brand>/', CardModelView.as_view()),
    path('cars/owner/', MyCarsView.as_view()),
    path('cars/owner/<int:pk>/', CarView.as_view())

]