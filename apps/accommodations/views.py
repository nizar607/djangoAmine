# apps/accommodations/views.py
from django.views.generic import TemplateView
from web_project import TemplateLayout
from .models import Hotel, RentalHouse , Reservation_Accommodation
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import json



GEMINI_API_KEY = 'AIzaSyDJlRpc1PnUvZUYCCe7Whg2cMNhBoi16H4'

def get_accommodation_suggestions(query):  # Accept query as a parameter
    
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}'

    payload = {
        "contents": {
            "parts": [
                {"text": query}
            ]
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}



def fetch_accommodation_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        data = get_accommodation_suggestions(query)
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'No query provided'}, status=400)
    

class AccommodationListView(TemplateView):
    def get_context_data(self, **kwargs):
        # Initialize context using TemplateLayout
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['hotels'] = Hotel.objects.all()
        context['rental_houses'] = RentalHouse.objects.all()
        return context

# apps/accommodations/views.py

class UserReservationsView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['reservations'] = Reservation_Accommodation.objects.filter(user=self.request.user)
        return context



@csrf_protect
def create_reservation(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'User not authenticated'}, status=401)

        accommodation_name = request.POST.get('accommodation_name')
        accommodation_type = request.POST.get('accommodation_type')
        phone = request.POST.get('phone')   
        accommodation_location = request.POST.get('accommodation_location')
        start_date = request.POST.get('start_date')  # Start date
        end_date = request.POST.get('end_date')      # End date
        num_guests = request.POST.get('num_guests')
        total_price = request.POST.get('total_price')
        
        

        if not (accommodation_name and accommodation_location and start_date and end_date and num_guests and accommodation_type and phone and total_price):
            return JsonResponse({'success': False, 'error': 'Missing data in request'}, status=400)

        try:
            reservation = Reservation_Accommodation.objects.create(
                user=request.user,  # Add the logged-in user
                accommodation_name=accommodation_name,
                accommodation_type = accommodation_type,
                phone = phone,
                accommodation_location=accommodation_location,
                start_date =  start_date,
                end_date = end_date,              
                num_guests=int(num_guests),
                total_price=total_price
            )
            return JsonResponse({'success': True, 'reservation_id': reservation.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



@login_required
def user_reservations(request):
    reservations = Reservation_Accommodation.objects.filter(user=request.user)
    # Pass `reservations` to the template for rendering
    return render(request, 'accommodation_reservation.html', {'reservations': reservations})


from datetime import datetime

@csrf_exempt
def update_reservation(request, id):
    if request.method == 'POST':
        try:
            reservation = Reservation_Accommodation.objects.get(id=id)

            # Retrieve and update the start and end dates
            start_date = request.POST.get('reservation_start_date')
            end_date = request.POST.get('reservation_end_date')
            
            # Calculate the number of days between the start and end dates
            if start_date and end_date:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                num_days = (end_date_obj - start_date_obj).days
                print("reservation here",reservation)
                
                price_per_night = reservation.total_price / max((reservation.end_date - reservation.start_date).days, 1) / int(reservation.num_guests)
                reservation.num_guests = request.POST.get('num_guests')
                new_total_price = num_days * price_per_night * int(reservation.num_guests)
                reservation.total_price = new_total_price

            # Save the new dates and total price
            reservation.start_date = start_date
            reservation.end_date = end_date
            reservation.save()

            return JsonResponse({'success': True})
        except Reservation_Accommodation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reservation not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def delete_reservation(request, id):
    if request.method == 'POST':
        try:
            reservation = Reservation_Accommodation.objects.get(id=id)
            reservation.delete()
            return JsonResponse({'success': True})
        except Reservation_Accommodation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reservation not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def get_reservation_byid(request, id):
    try:
        # Retrieve the reservation object by ID
        reservation = Reservation_Accommodation.objects.get(id=id)
        
        # Prepare the data to return in JSON format
        data = {
            'success': True,
            'start_date': reservation.start_date.strftime('%Y-%m-%d'),  # Format date as 'YYYY-MM-DD'
            'end_date': reservation.end_date.strftime('%Y-%m-%d'),  # Format date as 'YYYY-MM-DD'
            'num_guests': reservation.num_guests,
            'accommodation_name': reservation.accommodation_name,
            'accommodation_type': reservation.accommodation_type,
            'accommodation_location': reservation.accommodation_location,
            'phone': reservation.phone,
            'num_guests': reservation.num_guests,
            'created_at': reservation.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime
        }
        
        return JsonResponse(data)
    except Reservation_Accommodation.DoesNotExist:
        # If reservation is not found, return an error response
        return JsonResponse({'success': False, 'error': 'Reservation not found'})