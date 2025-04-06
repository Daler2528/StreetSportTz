from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import User, Stadium, Booking, Payment, StadiumStatistic

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'phone_number']
    search_fields = ['username', 'role']

@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'capacity', 'owner']
    search_fields = ['name', 'location']

from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('stadium', 'user', 'date', 'start_time', 'end_time', 'is_confirmed')

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # clean() metodi bilan to‘liq validatsiya
        except ValidationError as e:
            form.add_error(None, e)  # xatolikni forma orqali qaytar
            return
        super().save_model(request, obj, form, change)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_method', 'payment_date']
    list_filter = ['payment_method']

@admin.register(StadiumStatistic)
class StadiumStatisticAdmin(admin.ModelAdmin):
    list_display = ['stadium', 'date', 'total_bookings', 'total_income']
