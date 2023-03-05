from rest_framework import serializers
from .models import NewUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'email', 'user_name', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = NewUser.objects.create_user(**validated_data)

        return user

    def getUser(self, validated_data):
        user = NewUser.objects.get(id=validated_data[id])

        return user

