from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from my_selling_site.const import DEFAULT_CHAR_MAX_LEN


class User(AbstractUser):
    phone = PhoneNumberField(unique=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

class Region(models.Model):
    title = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)


class City(models.Model):
    title = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class District(models.Model):
    title = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class MetroStation(models.Model):
    title = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class House(models.Model):
    type = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    number = models.IntegerField()
    street = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN * 2)
    district = models.ForeignKey(District, on_delete=models.CASCADE)


class Apartment(models.Model):
    number = models.IntegerField()
    floor = models.IntegerField()
    entrance = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    square = models.FloatField()
    rooms_amount = models.IntegerField()
    description = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN * 5)
    seller_type = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    metro_station = models.ForeignKey(MetroStation, on_delete=models.CASCADE)


class UserApartmentFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)


# Надо будет потом вынести в константы длины строк (max_lenght) - done
