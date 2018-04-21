from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


# Create your models here.
# User will be extended from the default user classs


class Profile(models.Model):
    # Options to show to the user when adding a new room
    USER_TYPE_CHOICES = (
        (1, 'Customer'),
        (2, 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = CloudinaryField('profile picture')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class RoomType(models.Model):
    type_id = models.IntegerField()
    type_name = models.CharField(max_length=30)
    wifi = models.BooleanField(default=False)
    room_service = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    shuttle_service = models.BooleanField(default=False)
    mini_bar = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)

    class Meta:
        ordering = ["type_id", "type_name"]
        verbose_name = 'Room Type'
        verbose_name_plural = 'Room Types'

    def __str__(self):
        return self.type_name


class Room(models.Model):
    # Options to show to the user when adding a new room
    ROOM_TYPE_CHOICES = (
        (1, 'Executive'),
        (2, 'Deluxe'),
        (3, 'Presidential'),
        (4, 'Business'),
    )

    room_number = models.AutoField(primary_key=True)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, choices=ROOM_TYPE_CHOICES)
    occupied = models.BooleanField(default=False)
    price = models.IntegerField('Price of the room', help_text='Enter the price of the room')
    capacity = models.IntegerField()

    class Meta:
        ordering = ["room_number", "room_type"]
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return str(self.room_number)


class Booking(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)

    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField()

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'


class Image(models.Model):
    room_number = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='images')
    image_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1000)
    description = models.CharField(blank=True, max_length=1000)

    class Meta:
        unique_together = (('image_id', 'room_number'),)
