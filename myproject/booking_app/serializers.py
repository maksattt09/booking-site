from django.contrib.auth import authenticate

from .models import (Hotel,Country,UserProfile,Service,
                     City,HotelImage,Room,RoomImage,Review,Booking)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username', 'email', 'password', 'country')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
       model = UserProfile
       fields = ['first_name', 'last_name', 'user_image', 'user_role' ]

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
       model = UserProfile
       fields = '__all__'

class CountryProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_image','country_name']

class UserProfileReviewSerializers(serializers.ModelSerializer):
    country = CountryProfileSerializers()

    class Meta:
        model = UserProfile
        fields = ['first_name','country','user_image',]

class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image']

class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name',]

class HotelImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']

class HotelListSerializer(serializers.ModelSerializer):
    city = CityNameSerializer()
    hotel_image = HotelImageSerializers(many = True,read_only = True)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name','hotel_image','city','hotel_stars','description']


class HotelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_image','service_name']

class RoomListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id","price", "room_number", "room_type","room_status","description"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    user = UserProfileReviewSerializers()

    class Meta:
        model = Review
        fields = ["id","comment","created_date",'user']

class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_image = HotelImageSerializers(many=True, read_only=True)
    country = CountrySerializers()
    city = CityNameSerializer()
    hotel_service = ServiceSerializers(many=True)
    hotel_rooms = RoomListSerializers(many=True, read_only=True)
    hotel_reviews = ReviewSerializers(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'country', 'city', 'hotel_stars',
            'street', 'postal_code','hotel_image', 'description', 'hotel_service',
                  'hotel_rooms','get_avg_rating','get_count_people','hotel_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()


    def get_count_people(self,obj):
        return obj.get_count_people()


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class CityDetailSerializer(serializers.ModelSerializer):
    hotels = HotelListSerializer(many=True,read_only=True)
    class Meta:
        model = City
        fields = ['city_name', 'hotels']


class RoomImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']


class RoomDetailSerializers(serializers.ModelSerializer):
    room_photos = RoomImageSerializers(many=True,read_only=True)

    class Meta:
        model = Room
        fields = ["id","price", "room_number", "room_type","room_status","description",'room_photos']



class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'