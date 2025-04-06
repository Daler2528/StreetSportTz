from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking, Stadium

@receiver(post_save, sender=Booking)
def update_stadium_bron_on_save(sender, instance, created, **kwargs):
    stadium = instance.stadium
    if stadium.bookings.exists():
        stadium.bron = True
    else:
        stadium.bron = False
    stadium.save()

@receiver(post_delete, sender=Booking)
def update_stadium_bron_on_delete(sender, instance, **kwargs):
    stadium = instance.stadium
    if stadium.bookings.exists():
        stadium.bron = True
    else:
        stadium.bron = False
    stadium.save()
