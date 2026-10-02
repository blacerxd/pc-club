from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Club, ClubWorkingHours, Zone, ZonePriceModifier, Peripheral, HardwareProfile, Workstation
from .serializers import ClubSerializer, ClubWorkingHoursSerializer, ZoneSerializer, ZonePriceModifierSerializer, PeripheralSerializer, HardwareProfileSerializer, WorkstationSerializer

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ClubWorkingHoursViewSet(viewsets.ModelViewSet):
    queryset = ClubWorkingHours.objects.all()
    serializer_class = ClubWorkingHoursSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ZonePriceModifierViewSet(viewsets.ModelViewSet):
    queryset = ZonePriceModifier.objects.all()
    serializer_class = ZonePriceModifierSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PeripheralViewSet(viewsets.ModelViewSet):
    queryset = Peripheral.objects.all()
    serializer_class = PeripheralSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class HardwareProfileViewSet(viewsets.ModelViewSet):
    queryset = HardwareProfile.objects.all()
    serializer_class = HardwareProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class WorkstationViewSet(viewsets.ModelViewSet):
    queryset = Workstation.objects.all()
    serializer_class = WorkstationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

