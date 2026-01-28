from django_filters import FilterSet
from .models import Room

class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'room_type': ['exact'],
            'room_status': ['exact'],
            'price': ['gt','lt']
        }
