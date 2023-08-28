from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    title = models.CharField(max_length=60)
    phone = models.IntegerField()
    email = models.CharField(max_length=30)


class Region(models.Model):
    title = models.CharField(max_length=30)


class City(models.Model):
    title = models.CharField(max_length=30)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class District(models.Model):
    title = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class MetroStation(models.Model):
    title = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class House(models.Model):
    _type = models.CharField(max_length=30)
    number = models.IntegerField()
    street = models.IntegerField
    district = models.ForeignKey(District, on_delete=models.CASCADE)


class Apartment(models.Model):
    number = models.IntegerField()
    floor = models.IntegerField()
    entrance = models.CharField(max_length=30)
    square = models.IntegerField()
    rooms_amount = models.IntegerField()
    description = models.CharField(max_length=150)
    seller_type = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    metro_station = models.ForeignKey(MetroStation, on_delete=models.CASCADE)


class UserApartmentFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

