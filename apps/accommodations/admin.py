from django.contrib import admin
from .models import Hotel, RentalHouse , Reservation_Accommodation
# Register your models here.
# admin.py



@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price_per_night', 'availability', 'num_rooms', 'has_wifi', 'has_pool', 'accommodation_type')
    list_filter = ('location', 'availability', 'has_wifi', 'has_pool')
    search_fields = ('name', 'location')

@admin.register(RentalHouse)
class RentalHouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price_per_night', 'availability', 'num_bedrooms', 'has_kitchen', 'has_garage', 'accommodation_type')
    list_filter = ('location', 'availability', 'has_kitchen', 'has_garage')
    search_fields = ('name', 'location')


@admin.register(Reservation_Accommodation)
class ReservationAccommodationAdmin(admin.ModelAdmin):
    list_display = ('accommodation_name','accommodation_type', 'accommodation_location', 'start_date','end_date', 'num_guests', 'created_at')
    list_filter = ('accommodation_location', 'start_date', 'end_date') 
    search_fields = ('accommodation_name', 'accommodation_location')