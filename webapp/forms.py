from django import forms
from .models import FAQ, Order, User


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['description', 'delivery_type']
        labels = {
            'description': 'Детали', 'delivery_type': 'Способ доставки'
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'second_name', 'last_name', 'phone', 'email', 'birthdate', 'main_address']
        labels = {
            'name': 'Имя', 'second_name': 'Отчество', 'last_name': 'Фамилия', 'phone': 'Телефон',
            'email': 'Почта', 'birthdate': 'Дата рождения', 'main_address': 'Основной адрес'
        }
