from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class Car(models.Model):
    """Модель автомобиля для симулятора каршеринга"""
    
    CAR_CLASSES = [
        ('economy', 'Эконом'),
        ('comfort', 'Комфорт'),
        ('business', 'Бизнес'),
        ('premium', 'Премиум'),
    ]
    
    FUEL_TYPES = [
        ('gasoline', 'Бензин'),
        ('diesel', 'Дизель'),
        ('electric', 'Электро'),
        ('hybrid', 'Гибрид'),
    ]
    
    TRANSMISSION_TYPES = [
        ('manual', 'Механика'),
        ('automatic', 'Автомат'),
        ('robot', 'Робот'),
    ]
    
    model = models.CharField('Модель', max_length=100, db_index=True)
    brand = models.CharField('Марка', max_length=50, default='Toyota')
    color = models.CharField('Цвет', max_length=50)
    license_plate = models.CharField(
        'Госномер', 
        max_length=20, 
        unique=True,
        validators=[RegexValidator(r'^[А-Я]{1}\d{3}[А-Я]{2}\d{2,3}$', 'Введите корректный госномер')]
    )
    fuel_level = models.IntegerField(
        'Уровень топлива', 
        default=100, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Проценты'
    )
    fuel_type = models.CharField('Тип топлива', max_length=20, choices=FUEL_TYPES, default='gasoline')
    transmission = models.CharField('КПП', max_length=20, choices=TRANSMISSION_TYPES, default='automatic')
    price_per_minute = models.DecimalField(
        'Цена за минуту', 
        max_digits=5, 
        decimal_places=2, 
        default=10,
        validators=[MinValueValidator(Decimal('1.00'))]
    )
    car_class = models.CharField('Класс авто', max_length=20, choices=CAR_CLASSES, default='economy', db_index=True)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    is_available = models.BooleanField('Доступен', default=True, db_index=True)
    mileage = models.IntegerField('Пробег', default=0, help_text='км')
    rating = models.DecimalField(
        'Рейтинг', 
        max_digits=2, 
        decimal_places=1, 
        default=5.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    image = models.ImageField('Фото', upload_to='cars/', null=True, blank=True)
    last_service_date = models.DateField('Последнее ТО', null=True, blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-is_available', 'brand', 'model']
        indexes = [
            models.Index(fields=['is_available', 'car_class']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate}"
    
    def get_fuel_percentage(self):
        """Возвращает уровень топлива в процентах с цветом"""
        if self.fuel_level >= 70:
            return {'value': self.fuel_level, 'color': 'success', 'icon': 'fa-battery-full'}
        elif self.fuel_level >= 30:
            return {'value': self.fuel_level, 'color': 'warning', 'icon': 'fa-battery-half'}
        else:
            return {'value': self.fuel_level, 'color': 'danger', 'icon': 'fa-battery-empty'}
    
    def get_price_per_hour(self):
        """Возвращает цену за час"""
        return self.price_per_minute * 60
    
    def get_price_per_day(self):
        """Возвращает цену за день (8 часов)"""
        return self.get_price_per_hour() * 8

class Trip(models.Model):
    """Модель поездки"""
    
    TRIP_STATUS = [
        ('planned', 'Запланирована'),
        ('active', 'Активна'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        verbose_name='Автомобиль',
        related_name='trips'
    )
    start_time = models.DateTimeField('Время начала', auto_now_add=True)
    end_time = models.DateTimeField('Время окончания', null=True, blank=True)
    total_cost = models.DecimalField(
        'Стоимость', 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    is_active = models.BooleanField('Активна', default=True, db_index=True)
    status = models.CharField('Статус', max_length=20, choices=TRIP_STATUS, default='active')
    start_location_lat = models.FloatField('Широта начала', null=True, blank=True)
    start_location_lng = models.FloatField('Долгота начала', null=True, blank=True)
    end_location_lat = models.FloatField('Широта окончания', null=True, blank=True)
    end_location_lng = models.FloatField('Долгота окончания', null=True, blank=True)
    distance_km = models.FloatField('Пройденное расстояние', null=True, blank=True, help_text='км')
    fuel_consumed = models.FloatField('Потрачено топлива', null=True, blank=True, help_text='л')
    rating = models.IntegerField(
        'Оценка поездки', 
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['is_active', 'status']),
            models.Index(fields=['car', '-start_time']),
        ]
    
    def __str__(self):
        return f"Поездка {self.car.model} от {self.start_time.strftime('%d.%m.%Y %H:%M')}"
    
    def get_duration(self):
        """Возвращает продолжительность поездки"""
        if not self.end_time:
            return timezone.now() - self.start_time
        return self.end_time - self.start_time
    
    def get_duration_minutes(self):
        """Возвращает продолжительность в минутах"""
        duration = self.get_duration()
        return int(duration.total_seconds() / 60)
    
    def calculate_cost(self):
        """Рассчитывает стоимость поездки"""
        if not self.end_time:
            return None
        minutes = self.get_duration_minutes()
        return Decimal(minutes) * self.car.price_per_minute
    
    def save(self, *args, **kwargs):
        """Переопределенный метод сохранения"""
        if self.end_time and not self.total_cost:
            self.total_cost = self.calculate_cost()
            self.is_active = False
            self.status = 'completed'
            
            # Освобождаем автомобиль после завершения поездки
            self.car.is_available = True
            self.car.save()
            
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    """Профиль пользователя"""
    
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField('Телефон', max_length=20, unique=True)
    driver_license = models.CharField('Вод. удостоверение', max_length=20, unique=True)
    balance = models.DecimalField('Баланс', max_digits=10, decimal_places=2, default=0)
    total_trips = models.IntegerField('Всего поездок', default=0)
    total_spent = models.DecimalField('Всего потрачено', max_digits=12, decimal_places=2, default=0)
    rating = models.DecimalField(
        'Рейтинг', 
        max_digits=2, 
        decimal_places=1, 
        default=5.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    is_verified = models.BooleanField('Верифицирован', default=False)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    last_active = models.DateTimeField('Последняя активность', auto_now=True)
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
    
    def add_trip_cost(self, cost):
        """Добавляет стоимость поездки в статистику"""
        self.total_trips += 1
        self.total_spent += cost
        self.save()

class Payment(models.Model):
    """Модель платежа"""
    
    PAYMENT_STATUS = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершен'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возврат'),
    ]
    
    PAYMENT_METHOD = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличные'),
        ('bonus', 'Бонусы'),
    ]
    
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    status = models.CharField('Статус', max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_METHOD)
    transaction_id = models.CharField('ID транзакции', max_length=100, unique=True, null=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Платеж {self.amount} руб. за поездку {self.trip.id}"

class CarReview(models.Model):
    """Отзыв об автомобиле"""
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField('Комментарий', max_length=500)
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['user', 'trip']
    
    def __str__(self):
        return f"Отзыв от {self.user} на {self.car}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Обновляем рейтинг автомобиля
        reviews = self.car.reviews.all()
        if reviews.exists():
            avg_rating = sum(r.rating for r in reviews) / reviews.count()
            self.car.rating = avg_rating
            self.car.save()

class Promotion(models.Model):
    """Акции и скидки"""
    
    code = models.CharField('Промокод', max_length=50, unique=True)
    description = models.TextField('Описание')
    discount_percent = models.IntegerField('Скидка %', validators=[MinValueValidator(1), MaxValueValidator(100)])
    min_trip_cost = models.DecimalField('Мин. стоимость поездки', max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField('Действует с')
    valid_to = models.DateTimeField('Действует до')
    max_uses = models.IntegerField('Макс. использований', default=1)
    current_uses = models.IntegerField('Текущ. использований', default=0)
    is_active = models.BooleanField('Активна', default=True)
    
    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
    
    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"
    
    def is_valid(self):
        """Проверяет, действительна ли акция"""
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_to and 
                self.current_uses < self.max_uses)