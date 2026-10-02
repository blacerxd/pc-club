from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Booking, BookingStatusLog, Waitlist
from .serializers import BookingSerializer, BookingStatusLogSerializer, WaitlistSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookingStatusLogViewSet(viewsets.ModelViewSet):
    queryset = BookingStatusLog.objects.all()
    serializer_class = BookingStatusLogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class WaitlistViewSet(viewsets.ModelViewSet):
    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

