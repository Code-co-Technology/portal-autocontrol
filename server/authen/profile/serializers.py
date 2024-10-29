from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import MaxLengthValidator

from authen.models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'first_name', 'last_name', 'avatar']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, max_length=30, validators=[UniqueValidator(queryset=CustomUser.objects.all()),
            MaxLengthValidator(limit_value=20, message="Длина адреса электронной почты не может превышать 30 символов.")],)
    avatar = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    phone = serializers.CharField(required=True, max_length=15, validators=[UniqueValidator(queryset=CustomUser.objects.all()),
            MaxLengthValidator(limit_value=20, message="Длина Телефон не может превышать 15 символов.")],)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'first_name', 'last_name', 'avatar']
    
    def update(self, instance, validated_data):
        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)

        if instance.avatar == None:
            instance.avatar = self.context.get("avatar")
        else:
            instance.avatar = validated_data.get("avatar", instance.avatar)

        instance.save()
        return instance
