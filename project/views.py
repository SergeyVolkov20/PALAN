from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import random
from .models import Car, Trip
from .forms import CarFilterForm

def index(request):
    """Главная страница с картой и списком автомобилей"""
    cars = Car.objects.filter(is_available=True)
    form = CarFilterForm(request.GET or None)
    
    if form.is_valid():
        if form.cleaned_data['car_class']:
            cars = cars.filter(car_class=form.cleaned_data['car_class'])
        if form.cleaned_data['min_price']:
            cars = cars.filter(price_per_minute__gte=form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
            cars = cars.filter(price_per_minute__lte=form.cleaned_data['max_price'])
        if form.cleaned_data['min_fuel']:
            cars = cars.filter(fuel_level__gte=form.cleaned_data['min_fuel'])
    
    context = {
        'cars': cars,
        'form': form,
    }
    return render(request, 'index.html', context)

def get_cars_json(request):
    """API для получения списка автомобилей в формате JSON"""
    cars = Car.objects.filter(is_available=True)
    cars_data = []
    for car in cars:
        cars_data.append({
            'id': car.id,
            'model': car.model,
            'color': car.color,
            'license_plate': car.license_plate,
            'fuel_level': car.fuel_level,
            'price_per_minute': float(car.price_per_minute),
            'car_class': car.car_class,
            'latitude': float(car.latitude),
            'longitude': float(car.longitude),
        })
    return JsonResponse({'cars': cars_data})

@csrf_exempt
def start_trip(request):
    """Начать поездку"""
    if request.method == 'POST':
        data = json.loads(request.body)
        car_id = data.get('car_id')
        
        car = get_object_or_404(Car, id=car_id)
        
        if not car.is_available:
            return JsonResponse({'error': 'Автомобиль недоступен'}, status=400)
        
        trip = Trip.objects.create(
            car=car,
            is_active=True
        )
        
        car.is_available = False
        car.save()
        
        return JsonResponse({
            'success': True,
            'trip_id': trip.id,
            'start_time': trip.start_time.isoformat()
        })

@csrf_exempt
def end_trip(request):
    """Завершить поездку"""
    if request.method == 'POST':
        data = json.loads(request.body)
        trip_id = data.get('trip_id')
        final_cost = data.get('final_cost')
        
        trip = get_object_or_404(Trip, id=trip_id)
        
        trip.end_time = timezone.now()
        trip.total_cost = final_cost
        trip.is_active = False
        trip.save()
        
        car = trip.car
        car.is_available = True
        car.save()
        
        return JsonResponse({'success': True})

def init_data(request):
    """Инициализация тестовыми данными (только для разработки)"""
    base_lat, base_lon = 61.254, 73.396
    
    cars_data = [
        {
            'model': 'Kia Rio',
            'color': 'Белый',
            'license_plate': 'А001AA 86',
            'fuel_level': 85,
            'price_per_minute': 10,
            'car_class': 'economy',
        },
        {
            'model': 'Hyundai Solaris',
            'color': 'Черный',
            'license_plate': 'В002BB 86',
            'fuel_level': 92,
            'price_per_minute': 11,
            'car_class': 'economy',
        },
        {
            'model': 'Skoda Octavia',
            'color': 'Серый',
            'license_plate': 'Е003ЕЕ 86',
            'fuel_level': 78,
            'price_per_minute': 15,
            'car_class': 'comfort',
        },
        {
            'model': 'Toyota Camry',
            'color': 'Серебристый',
            'license_plate': 'К004КК 86',
            'fuel_level': 95,
            'price_per_minute': 18,
            'car_class': 'comfort',
        },
        {
            'model': 'BMW 3 Series',
            'color': 'Синий',
            'license_plate': 'М005ММ 86',
            'fuel_level': 70,
            'price_per_minute': 25,
            'car_class': 'business',
        },
        {
            'model': 'Mercedes E-Class',
            'color': 'Черный',
            'license_plate': 'О006ОО 86',
            'fuel_level': 88,
            'price_per_minute': 30,
            'car_class': 'business',
        },
    ]

    for i, car_data in enumerate(cars_data):
        lat_offset = (random.random() - 0.5) * 0.05
        lon_offset = (random.random() - 0.5) * 0.05
        
        Car.objects.get_or_create(
            license_plate=car_data['license_plate'],
            defaults={
                **car_data,
                'latitude': base_lat + lat_offset,
                'longitude': base_lon + lon_offset,
            }
        )
    
    return JsonResponse({'success': True, 'message': 'Данные инициализированы'})