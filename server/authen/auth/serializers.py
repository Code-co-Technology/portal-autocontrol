from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from authen.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    username = serializers.CharField(max_length=20, min_length=1, required=False, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "phone", "password", "confirm_password"]

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Электронная почта должна быть уникальной. Этот адрес электронной почты принадлежит другому пользователю.'})

        if CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({'error': 'Номер телефона должен быть уникальным. Этот номер телефона принадлежит другому пользователю.'})

        return attrs

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        if validated_data["password"] != validated_data["confirm_password"]:
            raise serializers.ValidationError({"error": "Подтверждение пароля не соответствует паролю"})
        validated_data.pop("confirm_password")
        create = CustomUser.objects.create_user(**validated_data)
        return create


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=2)
    password = serializers.CharField(max_length=50, min_length=1)

    class Meta:
        model = CustomUser
        fields = ["username", "password"]
        read_only_fields = ("username",)

    def validate(self, data):
        if self.context.get("request") and self.context["request"].method == "POST":
            allowed_keys = set(self.fields.keys())
            input_keys = set(data.keys())
            extra_keys = input_keys - allowed_keys
            if extra_keys:
                raise serializers.ValidationError(f"Additional keys are not allowed: {', '.join(extra_keys)}")
        return data
