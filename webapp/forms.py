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
    # TODO: smart password change
    class Meta:
        model = User
        fields = ['name', 'second_name', 'last_name', 'phone', 'email', 'birthdate', 'main_address']
        labels = {
            'name': 'Имя', 'second_name': 'Отчество', 'last_name': 'Фамилия', 'phone': 'Телефон',
            'email': 'Почта', 'birthdate': 'Дата рождения', 'main_address': 'Основной адрес'
        }


class SignUpForm(forms.ModelForm):
    help_text = 'Обязательное поле'
    # TODO: change max_length
    # TODO: password validadors, password help - сделать inline
    # TODO: link properly with database
    # TODO: протестить функции
    username = forms.CharField(max_length=20, help_text=help_text, label='Логин')
    password = forms.CharField(max_length=50, help_text=help_text, label='Пароль', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=150, help_text=help_text, label='Почта')
    phone = forms.CharField(max_length=20, help_text=help_text, label='Телефон')
    name = forms.CharField(max_length=50, help_text=help_text, label='Имя')
    last_name = forms.CharField(max_length=50, help_text=help_text, label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'phone', 'last_name']
        labels = {
            'username': 'Логин', 'password': 'Пароль', 'name': 'Имя',
            'last_name': 'Фамилия', 'email': 'Почта', 'phone': 'Телефон'
        }

    # DO form cleaning here
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError('Указанное имя пользователя уже используется')
    #     return username
    #
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("Указанная почта уже используется")
    #     return email
    #
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #
    #     # Сheck password length
    #     if len(password) < 8:
    #         raise ValidationError("Длина пароля должна быть не менее 8 символов")
    #     # Сheck for number and letters is password
    #     if password.isalpha() or password.isnumeric():
    #         raise ValidationError("Пароль должен содержать цифры и буквы")
    #
    #     return password
    #
    # def clean_phone_number(self):
    #     phone = self.cleaned_data.get('phone')
    #     if phone == "":
    #         raise ValidationError("Обязательное поле")
    #     else:
    #         if User.objects.filter(phone=phone):
    #             raise ValidationError("Указанный номер телефона уже используется")
    #     return phone
