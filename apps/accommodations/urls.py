# apps/accommodations/urls.py
from django.urls import path
from .views import AccommodationListView , create_reservation , UserReservationsView , fetch_accommodation_suggestions , update_reservation , delete_reservation , get_reservation_byid

urlpatterns = [
    path(
        'list/', 
        AccommodationListView.as_view(template_name='accommodation_list.html'), 
        name='accommodation_list'
    ),
     path(
        'create_reservation/', 
        create_reservation, 
        name='create_reservation'
    ),
    path('my_reservations/',
         UserReservationsView.as_view(template_name='accommodation_reservation.html'),
         name='my_reservations'
         ),
    path(
        'suggestions/', 
        fetch_accommodation_suggestions, 
        name='fetch-suggestions'
    ),
    path('reservation/<int:id>/update', update_reservation, name='update_reservation'),
    path('reservation/<int:id>/delete', delete_reservation, name='delete_reservation'),
    path('reservation/<int:id>/get', get_reservation_byid, name='get_reservation'),
    

]
