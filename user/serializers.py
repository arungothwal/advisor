from rest_framework import serializers
from .models import *


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Advisor
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'advisor_id', 'user_id', 'booking_time']


"""nested serializer for booking details"""


class GetBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=['id', 'user_id', 'booking_time']


class GetAdvisorsSerializer(serializers.ModelSerializer):
    booking = GetBookingSerializer(many=True)

    class Meta:
        model=Advisor
        fields=['id', 'name', 'pic', 'booking']