from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from car_app.models import CarBrand, CarModel, Cars


class RepostCardModel(admin.TabularInline):
    model = CarModel
    extra = 1
    min_num = 1


class AdminCardBrand(admin.ModelAdmin):
    inlines = [
        RepostCardModel
    ]
    list_display = ['id', 'name']

admin.site.register(CarBrand, AdminCardBrand)


class AdminCardModel(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(CarModel, AdminCardModel)


class AdminCard(admin.ModelAdmin):
    list_display = ['id', 'car_model', 'owner']

admin.site.register(Cars, AdminCard)