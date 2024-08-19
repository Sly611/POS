from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser

class CreateSuperUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("passwords must match")
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        user = CustomUser.objects.create_superuser(**validated_data, password=password)
        return user
    

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("passwords must match")
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user