from django import forms
from .models import UserFeedback, Order, User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


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
    # TODO: нужны действия, когда нет логина в аккаунт
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


class SignUpForm(UserCreationForm):
    help_text = 'Обязательное поле'
    # TODO: change max_length
    # TODO: password validadors, password help
    # TODO: link properly with database
    # TODO: протестить функции
    email = forms.EmailField(max_length=150, help_text=help_text, label='Почта')
    phone = forms.CharField(max_length=20, help_text=help_text, label='Телефон')
    name = forms.CharField(max_length=50, help_text=help_text, label='Имя')

    class Meta:
        model = User
        fields = ['username', 'password1', 'name', 'second_name', 'last_name', 'email', 'phone']
        labels = {
            'username': 'Логин', 'password': 'Пароль',
            'name': 'Имя', 'email': 'Почта', 'phone': 'Телефон'
        }

    # DO form cleaning here
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Указанное имя пользователя уже используется')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Указанная почта уже используется")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Сheck password length
        if len(password) < 8:
            raise ValidationError("Длина пароля должна быть не менее 8 символов")
        # Сheck for number and letters is password
        if password.isalpha() or password.isnumeric():
            raise ValidationError("Пароль должен содержать цифры и буквы")

        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number == "":
            raise ValidationError("Обязательное поле")
        else:
            if User.objects.filter(phone_number=phone_number):
                raise ValidationError("Указанный номер телефона уже используется")
        return phone_number
