from rest_framework import serializers

from car_app.models import CarBrand, CarModel, Cars


class CarBarndSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBrand
        fields = ["id", "name"]


class CardModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = ["id", "name", "brand"]


class CarsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cars
        fields = [
            "id", 
            "vin", 
            "state_number",
            "year_issue",
            "weight",
            "current_mileage",
            "image",
            "car_brand",
            "car_model",
            "owner",
            "create_at"
        ]



class CarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    
    class Meta:
        model = Cars
        fields = [
            "id", 
            "vin", 
            "state_number",
            "year_issue",
            "weight",
            "current_mileage",
            "image",
            "car_brand",
            "car_model",
            "owner",
            "create_at"
        ]

    def create(self, validated_data):
        car = Cars.objects.create(**validated_data)
        car.owner = self.context.get("owner")
        car.save()
        return validated_data
    
    def update(self, instance, validated_data):
        instance.vin = validated_data.get("vin", instance.vin)
        instance.state_number = validated_data.get("state_number", instance.state_number)
        instance.year_issue = validated_data.get("year_issue", instance.year_issue)
        instance.weight = validated_data.get("weight", instance.weight)
        instance.current_mileage = validated_data.get("current_mileage", instance.current_mileage)
        instance.car_brand = validated_data.get("car_brand", instance.car_brand)
        instance.car_model = validated_data.get("car_model", instance.car_model)

        if instance.image == None:
            instance.image = self.context.get("image")
        else:
            instance.image = validated_data.get("image", instance.image)

        instance.save()
        return instance
