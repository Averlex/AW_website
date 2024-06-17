from django import forms
from .models import UserFeedback, Order, User


class FAQForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rate = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label='Оцените работу сервиса')
    text = forms.Textarea()

    class Meta:
        model = UserFeedback
        fields = ['text', 'rate']
        labels = {
            'text': 'Текст отзыва или вопрос, который вы хотели бы задать:', 'rate': ''
        }


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
