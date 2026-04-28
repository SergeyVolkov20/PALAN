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
    """Инициализация тестовыми данными (15 автомобилей)"""
    # Сначала удалим старые
    Car.objects.all().delete()
    
    base_lat, base_lon = 61.254, 73.396
    
    cars_data = [
        {'model': 'Kia Rio', 'color': 'Белый', 'plate': 'А123АА', 'fuel': 85, 'price': 10, 'class': 'economy'},
        {'model': 'Hyundai Solaris', 'color': 'Чёрный', 'plate': 'В456ВВ', 'fuel': 90, 'price': 11, 'class': 'economy'},
        {'model': 'Skoda Rapid', 'color': 'Серый', 'plate': 'С789СС', 'fuel': 82, 'price': 12, 'class': 'economy'},
        {'model': 'Lada Vesta', 'color': 'Синий', 'plate': 'Т321ТТ', 'fuel': 88, 'price': 9, 'class': 'economy'},
        {'model': 'Volkswagen Polo', 'color': 'Красный', 'plate': 'М654ММ', 'fuel': 76, 'price': 11, 'class': 'economy'},
        {'model': 'Renault Logan', 'color': 'Бежевый', 'plate': 'Н987НН', 'fuel': 91, 'price': 10, 'class': 'economy'},
        {'model': 'Skoda Octavia', 'color': 'Графит', 'plate': 'О159ОО', 'fuel': 84, 'price': 15, 'class': 'comfort'},
        {'model': 'Toyota Camry', 'color': 'Чёрный', 'plate': 'К753КК', 'fuel': 92, 'price': 18, 'class': 'comfort'},
        {'model': 'Hyundai Elantra', 'color': 'Серебро', 'plate': 'Е246ЕЕ', 'fuel': 77, 'price': 16, 'class': 'comfort'},
        {'model': 'Kia K5', 'color': 'Тёмный', 'plate': 'Р369РР', 'fuel': 89, 'price': 17, 'class': 'comfort'},
        {'model': 'Mazda 6', 'color': 'Красный', 'plate': 'А951АА', 'fuel': 73, 'price': 16, 'class': 'comfort'},
        {'model': 'BMW 3', 'color': 'Синий', 'plate': 'Х357ХХ', 'fuel': 81, 'price': 26, 'class': 'business'},
        {'model': 'Mercedes C-Class', 'color': 'Серый', 'plate': 'У468УУ', 'fuel': 86, 'price': 28, 'class': 'business'},
        {'model': 'Audi A4', 'color': 'Белый', 'plate': 'С579СС', 'fuel': 79, 'price': 27, 'class': 'business'},
        {'model': 'Tesla Model 3', 'color': 'Чёрный', 'plate': 'Е681ЕЕ', 'fuel': 94, 'price': 29, 'class': 'business'},
    ]
    
    for car in cars_data:
        Car.objects.create(
            model=car['model'],
            color=car['color'],
            license_plate=car['plate'],
            fuel_level=car['fuel'],
            price_per_minute=car['price'],
            car_class=car['class'],
            latitude=base_lat + (random.random() - 0.5) * 0.04,
            longitude=base_lon + (random.random() - 0.5) * 0.04,
            is_available=True
        )
    
    return JsonResponse({'success': True, 'message': f'Добавлено {len(cars_data)} автомобилей'})

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