from django.db import models
from authen.models import CustomUser


class CarBrand(models.Model):
    name = models.CharField(max_length=250, verbose_name="Бренд")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "car_brand"
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марка автомобиля"


class CarModel(models.Model):
    name = models.CharField(max_length=250, verbose_name="Модель")
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Бренд")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "car_model"
        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модель автомобиля"


class Cars(models.Model):
    vin = models.CharField(max_length=250, verbose_name="VIN")
    state_number = models.CharField(max_length=250, verbose_name="Гос номер")
    year_issue = models.DateField(verbose_name="Год выпуска")
    weight = models.CharField(max_length=250, verbose_name="Масса")
    current_mileage = models.CharField(max_length=250, verbose_name="Текущий пробег")
    image = models.ImageField(upload_to="cars/", null=True, blank=True, verbose_name="Изображение автомобиля")
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, verbose_name="Марка автомобиля")
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name="Модель автомобиля")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Владеле: {self.owner.email} - Модель: {self.car_model.name}"

    class Meta:
        db_table = "cars"
        verbose_name = "Автомобили"
        verbose_name_plural = "Автомобили"
