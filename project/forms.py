from django import forms
from .models import Car

class CarFilterForm(forms.Form):
    """Форма для фильтрации автомобилей"""
    
    CAR_CLASSES = [
        ('', 'Все классы'),
        ('economy', 'Эконом'),
        ('comfort', 'Комфорт'),
        ('business', 'Бизнес'),
    ]
    
    car_class = forms.ChoiceField(choices=CAR_CLASSES, required=False, label='Класс авто')
    min_price = forms.DecimalField(required=False, label='Цена от', min_value=0)
    max_price = forms.DecimalField(required=False, label='Цена до', min_value=0)
    min_fuel = forms.IntegerField(required=False, label='Топливо от %', min_value=0, max_value=100)