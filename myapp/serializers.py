from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task,Comment,Kind
from django.core.exceptions import ValidationError


CustomUser = get_user_model()
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  # すべてのフィールドをシリアライズ

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
        ustomUser = get_user_model()
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    
class KindsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = '__all__'    