from django.db import models

class Car(models.Model):
    """Модель автомобиля для симулятора каршеринга"""
    
    CAR_CLASSES = [
        ('economy', 'Эконом'),
        ('comfort', 'Комфорт'),
        ('business', 'Бизнес'),
    ]
    
    model = models.CharField('Модель', max_length=100)
    color = models.CharField('Цвет', max_length=50)
    license_plate = models.CharField('Госномер', max_length=20, unique=True)
    fuel_level = models.IntegerField('Уровень топлива', default=100, help_text='Проценты')
    price_per_minute = models.DecimalField('Цена за минуту', max_digits=5, decimal_places=2, default=10)
    car_class = models.CharField('Класс авто', max_length=20, choices=CAR_CLASSES, default='economy')
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    is_available = models.BooleanField('Доступен', default=True)
    
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
    
    def __str__(self):
        return f"{self.model} - {self.license_plate}"

class Trip(models.Model):
    """Модель поездки"""
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    start_time = models.DateTimeField('Время начала', auto_now_add=True)
    end_time = models.DateTimeField('Время окончания', null=True, blank=True)
    total_cost = models.DecimalField('Стоимость', max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    
    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
    
    def __str__(self):
        return f"Поездка {self.car.model} от {self.start_time}"