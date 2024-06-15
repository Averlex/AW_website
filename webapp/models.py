import uuid

from django.db import models

_MAX_NAME = 50
_MAX_PHONE = 20
_MAX_ADDRESS = 150
_MAX_FEEDBACK = 500
_MAX_LINK = 100
_DEFAULT_MAX = 150
_MAX_TRACK_NUM = 20

class FAQ(models.Model):
    """
    FAQ table. Stores the pull of answers and questions for FAQ page
    """
    question = models.CharField(editable=False, max_length=_DEFAULT_MAX)
    answer = models.TextField(blank=True, db_default='', default='К сожалению, на этот вопрос пока не поступило ответа :(', editable=False)

    def __str__(self):
        return self.question

    class Meta:
        # Random ordering for FAQ table
        ordering = ['?']

    pass


class UserFeedback(models.Model):
    """
    User feedback table. Stores user scores, feedback text, as well as feedback sources and administration replies
    """
    _FEEDBACK_TYPE = {
        0: "Удобство заказа",
        1: "Функционал сайта",
        2: "Качество выполнения заказа",
        3: "Обратная связь и доставка",
    }

    _FEEDBACK_SOURCE = {
        0: "Сайт",
        1: "Сторонний ресурс",
        2: "Telegram",
        3: "Whatsapp",
        4: "E-mail"
    }

    # Base rate indicators
    rate = models.SmallIntegerField(default=0, db_default=0, blank=True, help_text='Пожалуйста, оцените работу сервиса')
    text = models.TextField(default='', db_default='', help_text='Поделитесь впечатлениями о работе сервиса', blank=True, max_length=_MAX_FEEDBACK)

    # Reply sent by carpentry employee
    reply = models.TextField(default='', db_default='', blank=True, max_length=_MAX_FEEDBACK)

    # Source link (outer sources only, e.g. ya.ru/some_forum/some_comment)
    source_link = models.CharField(default='', db_default='', blank=True, max_length=_MAX_LINK)

    # Categorical descriptionm
    feedback_type = models.SmallIntegerField(default=0, db_default=0, choices=_FEEDBACK_TYPE)
    feedback_source = models.SmallIntegerField(default=0, db_default=0, choices=_FEEDBACK_SOURCE)

    # DB linkage
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=False, db_default=None)

    def __str__(self):
        return self.rate.__str__() + ": " + self.text.__str__()

    class Meta:
        # Lower rates with details first
        # ordering = ['rate', '-text']
        constraints = [
            models.CheckConstraint(check=(models.Q(rate__gte=0) | ~models.Q(text='')), name='empty_feedback')
        ]

        pass

    pass


class User(models.Model):
    """
    Base user info
    """
    _USER_GROUP = {
        0: "Администратор",
        1: "Сотрудник магазина",
        2: "Довольный клиент",
    }

    _DELIVERY_TYPE = {
        0: "Самовывоз",
        1: "СДЭК",
    }

    # Administrator info
    user_group = models.SmallIntegerField(default=2, db_default=2, choices=_USER_GROUP)
    registration_date = models.DateField(auto_now_add=True, editable=False)

    # Personal info fields
    name = models.CharField(max_length=_MAX_NAME)
    second_name = models.CharField(max_length=_MAX_NAME)
    last_name = models.CharField(max_length=_MAX_NAME)
    phone = models.CharField(max_length=_MAX_PHONE, help_text='Основной контактный номер')
    email = models.EmailField(help_text='Действующий адрес электронной почты')
    birthdate = models.DateField(blank=True)

    # Possible delivery info
    pref_delivery_type = models.SmallIntegerField(default=0, db_default=0, blank=True, choices=_DELIVERY_TYPE)
    main_address = models.CharField(max_length=_MAX_ADDRESS, blank=True, default='', db_default='')

    def __str__(self):
        return self.name.__str__() + " " + self.second_name.__str__() + " " + self.last_name.__str__()


class Order(models.Model):
    """
    Base order info
    # TODO: check constraints on all dates
    # TODO: unify delivery types with User
    # TODO: total price (atm = agg by ProductList + price from Delivery)
    """
    _DELIVERY_TYPE = {
        0: "Самовывоз",
        1: "СДЭК",
    }

    _ORDER_STATUS = {
        0: "Новый заказ",
        1: "На уточнении",
        2: "Ожидает оплаты",
        3: "В работе",
        4: "Передается в доставку",
        5: "В доставке",
        6: "Завершен",
    }

    # Additional ID generated for user
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Date fields indicating stages of completion
    registration_date = models.DateTimeField(auto_now_add=True, editable=False)
    confirmation_date = models.DateTimeField(blank=True, editable=False)
    done_date = models.DateTimeField(blank=True, editable=False)
    received_date = models.DateTimeField(blank=True, editable=False)

    # Additional fields
    delivery_type = models.SmallIntegerField(default=0, db_default=0, blank=True, choices=_DELIVERY_TYPE)
    description = models.TextField(blank=True, max_length=_MAX_FEEDBACK, default='', db_default='')

    # DB linkage
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=False, db_default=None)
    delivery = models.ForeignKey("Delivery", on_delete=models.CASCADE, null=True, blank=False, db_default=None)

    def __str__(self):
        return self.order_id


class Delivery(models.Model):
    """
    Base delivery info
    """
    _CDEC_STATUS = {
        0: "Заказ покинул город отправления",
        1: "Заказ готов к выдаче",
        2: "Заказ вручен",
        3: "Заказ выдан на доставку курьеру",
        4: "Заказ не вручен",
    }

    # Additional ID generated for user
    delivery_id = models.CharField(max_length=_MAX_TRACK_NUM, unique=True)

    # Delivery address
    address = models.CharField(max_length=_MAX_ADDRESS, default='', db_default='')

    # Delivery status (expanded CDEC classification)
    status = models.SmallIntegerField(default=0, db_default=0, blank=True, choices=_CDEC_STATUS)

    # Additional comment for delivery
    description = models.TextField(blank=True, max_length=_MAX_FEEDBACK, default='', db_default='')

    # Delivery price
    price = models.FloatField(default=0, db_default=0)

    def __str__(self):
        return self.delivery_id
