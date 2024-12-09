from django.db import models
from django.contrib.auth.models import User

# Base Model for common fields
class Accommodation(models.Model):
    ACCOMMODATION_TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('rental', 'Rental House'),
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    accommodation_type = models.CharField(max_length=10, choices=ACCOMMODATION_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} ({self.get_accommodation_type_display()})"

# Model for Hotels
class Hotel(Accommodation):
    num_rooms = models.IntegerField()
    has_wifi = models.BooleanField(default=True)
    has_pool = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='hotel_photos/', blank=True, null=True)  # Field for hotel photo

# Model for Rental Houses
class RentalHouse(Accommodation):
    num_bedrooms = models.IntegerField()
    has_kitchen = models.BooleanField(default=True)
    has_garage = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='rental_photos/', blank=True, null=True)  # Field for rental house photo

# Model for Reservations  
class Reservation_Accommodation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    accommodation_name = models.CharField(max_length=255)
    accommodation_type = models.CharField(max_length=10)
    accommodation_location = models.CharField(max_length=255)
    start_date = models.DateField(null=True)  # Start date
    end_date = models.DateField(null=True)    # End date
    phone = models.CharField(max_length=15, blank=True, null=True)
    num_guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0 , null=True)
    
    def __str__(self):
        return f"{{'id': {self.id}, 'accommodation_name': '{self.accommodation_name}', 'accommodation_type': '{self.accommodation_type}', 'accommodation_location': '{self.accommodation_location}', 'start_date': '{self.start_date}', 'end_date': '{self.end_date}', 'num_guests': {self.num_guests}, 'total_price': {self.total_price}}}"
