from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


# Create your models here.
# User will be extended from the default user classs


class Profile(models.Model):
    # Options to show to the user when adding a new room

    CUSTOMER = 'CUSTOMER'
    ADMIN = 'ADMIN'
    USER_TYPE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (ADMIN, 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = CloudinaryField('profile picture', blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Room(models.Model):
    # Options to show to the user when adding a new room

    EXECUTIVE = 'EXECUTIVE'
    DELUXE = 'DELUXE'
    PRESIDENTIAL = 'PRESIDENTIAL'
    BUSINESS = 'BUSINESS'

    ROOM_TYPE_CHOICES = (
        (EXECUTIVE, 'Executive'),
        (DELUXE, 'Deluxe'),
        (PRESIDENTIAL, 'Presidential'),
        (BUSINESS, 'Business'),
    )

    room_number = models.AutoField(primary_key=True)
    room_type = models.CharField(choices=ROOM_TYPE_CHOICES, max_length=100)
    occupied = models.BooleanField(default=False)
    price = models.IntegerField('Price of the room', help_text='Enter the price of the room')
    capacity = models.IntegerField()
    wifi = models.BooleanField(default=False)
    room_service = models.BooleanField(default=False)
    electronic_safe = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)
    restaurant = models.BooleanField(default=False)
    pick_up = models.BooleanField(default=False)
    spa = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)

    class Meta:
        ordering = ["room_number", "room_type"]
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return str(self.room_type) + ' ' + str(self.room_number)


class Booking(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)

    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return str(self.user_id) + ' ' + str(self.room_id) + str(self.checkin_time)


class Image(models.Model):
    EXECUTIVE = 'EXECUTIVE'
    DELUXE = 'DELUXE'
    PRESIDENTIAL = 'PRESIDENTIAL'
    BUSINESS = 'BUSINESS'

    ROOM_TYPE_CHOICES = (
        (EXECUTIVE, 'Executive'),
        (DELUXE, 'Deluxe'),
        (PRESIDENTIAL, 'Presidential'),
        (BUSINESS, 'Business'),
    )
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES,
                                 help_text="Enter the room type for which you want to add an image")
    image_id = models.AutoField(primary_key=True)
    image = CloudinaryField('room image', blank=True)
    description = models.CharField(blank=True, max_length=1000)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', primary_key=True)
    rating = models.IntegerField()
    description = models.CharField(max_length=1000)
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return str(self.user_id) + ' ' + str(self.rating)