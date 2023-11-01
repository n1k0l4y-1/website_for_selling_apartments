from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from my_selling_site.const import DEFAULT_CHAR_MAX_LEN
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(phone=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        "username",
        max_length=150,
        unique=False,
        null=True,
        blank=True
    )
    phone = PhoneNumberField(unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'



class Region(models.Model):
    title = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)

    def __str__(self):
        return self.title



class City(models.Model):
    title = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.region.title})'


class District(models.Model):
    title = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.city.title})'


class MetroStation(models.Model):
    title = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.city.title})'


class House(models.Model):
    type = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    number = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    street = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN * 2)
    district = models.ForeignKey(District, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.street}, {self.number}'



class Apartment(models.Model):
    number = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=12)
    floor = models.IntegerField()
    entrance = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    square = models.FloatField()
    rooms_amount = models.IntegerField()
    description = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN * 5)
    seller_type = models.CharField(max_length=DEFAULT_CHAR_MAX_LEN)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    metro_station = models.ForeignKey(MetroStation, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.house} / {self.user}'


class Image(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='apartment_images')



class UserApartmentFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
