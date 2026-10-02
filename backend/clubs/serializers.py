from rest_framework import serializers
from .models import Club, ClubWorkingHours, Zone, ZonePriceModifier, Peripheral, HardwareProfile, Workstation

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

class ClubWorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubWorkingHours
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class ZonePriceModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZonePriceModifier
        fields = '__all__'

class PeripheralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peripheral
        fields = '__all__'

class HardwareProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareProfile
        fields = '__all__'

class WorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workstation
        fields = '__all__'

