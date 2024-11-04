import os
import django
import json

# Django muhitini sozlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # "config.settings" o'rniga o'zingizning loyihangizning settings faylini kiriting
django.setup()

from car_app.models import CarBrand, CarModel  # `car_app` bilan o'zingizning app nomingizni almashtiring

# JSON faylni o'qish
with open('cars.json', 'r') as file:
    data = json.load(file)

# Har bir brand va uning modellari uchun ma'lumotlarni bazaga qo'shish
for item in data:
    brand_name = item["brand"]
    models = item["models"]

    # CarBrand yaratish yoki mavjud bo'lsa olish
    brand, created = CarBrand.objects.get_or_create(name=brand_name)
    
    # CarModel yozuvlarini yaratish
    for model_name in models:
        CarModel.objects.get_or_create(name=model_name, brand=brand)

print("Data imported successfully!")
