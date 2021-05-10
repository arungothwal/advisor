from rest_framework import serializers
from .models import *


class Advisor_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Advisor
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'