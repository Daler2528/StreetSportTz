from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Stadium, Booking
from .permissions import IsAdminManagerOrOwner, IsAdminOrOwnerOfStadium, IsAdmin
from .serializer import StadiumModelSerializer, RegisterSerializer, LoginSerializer, BookingSerializer, \
    BookingListSerializer, BookingModelSerializer


# regitser qlish
@extend_schema(
    request=RegisterSerializer,
    tags=["User"]
)
class RegisterAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "phone_number": user.phone_number
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login qlish qaysi user yoki admin ili manager yoki owner niligini blish
@extend_schema(
    request=LoginSerializer,
    tags=["User"]
)
class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "phone_number": user.phone_number
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Stadiyon yaratish
@extend_schema(
    tags=['Stadium'])
class StadiumCreateAPIView(CreateAPIView):
    serializer_class = StadiumModelSerializer
    queryset = Stadium.objects.all()
    permission_classes = [IsAuthenticated, IsAdminManagerOrOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# stadiyon uchrish
@extend_schema(tags=['Stadium'])
class StadiumDeleteAPIView(DestroyAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumModelSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAdminOrOwnerOfStadium]


# stadiyon list
@extend_schema(
    tags=['Stadium'])
class StadiumListAPIView(ListAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumModelSerializer


# Bita Stadiyoni kurish
@extend_schema(
    tags=['Stadium'])
class StadiumDetailAPIView(RetrieveAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumModelSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAdminManagerOrOwner]


# Neshta stadiyon borligini kurish
@extend_schema(
    tags=["Ro'yxatdan o'tkan stadionlar soni"])
class StadiumCountView(APIView):

    def get(self, request):
        stadium_count = Stadium.objects.count()
        return Response({"total_stadiums": stadium_count})



# Faqad qaysi owner stadiyoni qushkanin kuroladi v uwa ownerga tegishli statistika kurnadi
@extend_schema(
    tags=["Stadion statistikasi va ma’lumotlarini ko‘rish (faqat o’zi ro’yxatdan o’tkazgan stadionlar)"]
)
class MyStadiumStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminManagerOrOwner]

    def get(self, request):
        user = request.user

        # Faqat o‘zi yaratgan stadionlarni olish
        stadiums = Stadium.objects.filter(owner=user)

        data = []
        for stadium in stadiums:
            bookings = stadium.bookings.all()
            total_bookings = bookings.count()
            total_income = sum(b.price for b in bookings)

            data.append({
                "stadium_name": stadium.name,
                "location": stadium.location,
                "capacity": stadium.capacity,
                "total_bookings": total_bookings,
                "total_income": total_income
            })

        return Response(data)


# Bu bron qilyodkan cod va bron qilyadkanda is_confirmed = False agar bron qlinsa u True ga uzgarad agar,
# adminga pul bermasa uni fieldni False qlip quysa uni yana bron qilsa buladi

@extend_schema(
    tags=["Booking"],
    request=BookingSerializer
)
class StadiumBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(user=request.user)

            # Agar stadion hali band qilinmagan bo‘lsa, bron flagini o‘zgartiramiz
            if not booking.stadium.bron:
                booking.stadium.bron = True
                booking.stadium.save()

            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Beta bron qlingan stadiyonlar ruyhati
@extend_schema(
    tags=["Bron Qlingan Stadiyonlar"]
)
class MyBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter().order_by('-date', '-start_time')


        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)

# Bu esa is_confirmed shuni fieldni uzgartrish uchun yozilgan api
@extend_schema(
    tags=["Update Fields"],
    request=BookingModelSerializer
)
class BookingUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    lookup_field = "pk"
