from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateTimeField, BooleanField
from django.db.models.enums import TextChoices
from django.core.exceptions import ValidationError as DjangoValidationError


# Create your models here.



class User(AbstractUser):
    class ROLE(TextChoices):
        ADMIN = "admin" , "Admin"
        OWNER = "owner" , "Owner" # statiyoni bosligi
        MANAGER = "manager" , "Manager"
        USER = "user" , "User"

    role = CharField(max_length=7 , choices=ROLE.choices,default=ROLE.USER)
    phone_number = CharField(max_length=15 , null=True , blank=True)

    def __str__(self):
        return self.username


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_stadiums")
    managers = models.ManyToManyField(User, related_name="managed_stadiums", blank=True)
    description = models.TextField(null=True, blank=True)
    bron = BooleanField(default=False)

    def __str__(self):
        return self.name



class Booking(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.stadium.name} - {self.date} ({self.start_time}-{self.end_time})"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Naqd'), ('online', 'Online')])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking} - {self.amount} {self.payment_method}"



class StadiumStatistic(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name="statistics")
    date = models.DateField()
    total_bookings = models.PositiveIntegerField(default=0)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Statistics for {self.stadium.name} on {self.date}"

