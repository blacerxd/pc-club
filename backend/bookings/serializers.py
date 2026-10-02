from rest_framework import serializers
from .models import Booking, BookingStatusLog, Waitlist

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingStatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingStatusLog
        fields = '__all__'

class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = '__all__'

