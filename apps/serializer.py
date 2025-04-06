from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import Stadium, User, Booking

User = get_user_model()

class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)
    password2 = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'phone_number', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError("Parollar mos emas.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise ValidationError("Login yoki parol noto‘g‘ri.")
        data['user'] = user
        return data

class StadiumModelSerializer(ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'
        read_only_fields = ['owner']



from rest_framework.serializers import ModelSerializer, ValidationError
from apps.models import Booking

class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'stadium', 'date', 'start_time', 'end_time',
            'price', 'is_confirmed'
        ]
        read_only_fields = ['is_confirmed']

    def validate(self, attrs):
        stadium = attrs['stadium']
        date = attrs['date']
        start_time = attrs['start_time']
        end_time = attrs['end_time']

        if start_time >= end_time:
            raise ValidationError(
                {"detail": "Boshlanish va tugash vaqtlari noto‘g‘ri kiritilgan!"}
            )

        # Faqat tasdiqlangan bronlar bilan to‘qnashuvni tekshiramiz
        conflict = Booking.objects.filter(
            stadium=stadium,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            is_confirmed=True
        ).exists()

        if conflict:
            raise ValidationError(
                {"detail": "Bu vaqt oralig‘ida tasdiqlangan bron mavjud!"}
            )

        return attrs

    def create(self, validated_data):
        validated_data['is_confirmed'] = True  # bron qilinganda darrov True
        return super().create(validated_data)





class BookingListSerializer(ModelSerializer):
    stadium_name = CharField(source='stadium.name', read_only=True)
    stadium_location = CharField(source='stadium.location', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'stadium_name', 'stadium_location',
            'date', 'start_time', 'end_time', 'price', 'is_confirmed'
        ]



class BookingModelSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ['is_confirmed']