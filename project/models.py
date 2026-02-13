from django.db import models


class Demo(models.Model):
    
    class Meta:
        managed = False
        db_table = 'demo'
        verbose_name = 'Демо'
        verbose_name_plural = 'Демо'

class User(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    data_joined = models.DateField(blank=True, null=True)  # или DateTimeField
    full_name = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Role(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'role'
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

class Visitor(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'visitor'
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'

class Staff(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'staff'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class GamingZone(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'gaming_zone'
        verbose_name = 'Игровая зона'
        verbose_name_plural = 'Игровые зоны'

class GamingStation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'gaming_station'
        verbose_name = 'Игровая станция'
        verbose_name_plural = 'Игровые станции'

class Shifts(models.Model):
    staff_id = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'shifts'
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'

class Visits(models.Model):
    booking_id = models.IntegerField(blank=True, null=True)
    visitor_id = models.IntegerField(blank=True, null=True)
    check_in_time = models.DateTimeField(blank=True, null=True)
    check_out_time = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'visits'
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'

class Bookings(models.Model):
    gaming_zone_id = models.IntegerField(blank=True, null=True)
    guest_count = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'bookings'
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

class ClubInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название клуба')
    address = models.TextField(verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    working_hours = models.CharField(max_length=100, blank=True, verbose_name='Часы работы')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Информация о клубе'
        verbose_name_plural = 'Информация о клубах'

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория оборудования'
        verbose_name_plural = 'Категории оборудования'

class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('room', 'Комната'),
        ('hardware', 'Комплектующие'),
        ('peripheral', 'Периферия'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Название')
    equipment_type = models.CharField(
        max_length=20, 
        choices=EQUIPMENT_TYPES,
        verbose_name='Тип оборудования'
    )
    specification = models.TextField(verbose_name='Характеристики')
    category = models.ForeignKey(
        EquipmentCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Категория'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    image = models.ImageField(
        upload_to='equipment/', 
        blank=True, 
        null=True,
        verbose_name='Изображение'
    )
    
    def __str__(self):
        return f"{self.name} ({self.get_equipment_type_display()})"
    
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

class WebsiteBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]
    
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    booking_date = models.DateField(verbose_name='Дата бронирования')
    booking_time = models.TimeField(verbose_name='Время бронирования')
    duration = models.IntegerField(verbose_name='Продолжительность (часы)', default=1)
    guests = models.IntegerField(verbose_name='Количество гостей', default=1)
    comments = models.TextField(verbose_name='Комментарии', blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return f"{self.full_name} - {self.booking_date} {self.booking_time}"
    
    class Meta:
        verbose_name = 'Бронирование с сайта'
        verbose_name_plural = 'Бронирования с сайта'
        ordering = ['-booking_date', '-booking_time']