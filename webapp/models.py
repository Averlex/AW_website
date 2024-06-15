from django.db import models

_MAX_NAME = 50
_MAX_PHONE = 20
_MAX_ADDRESS = 150
_MAX_FEEDBACK = 500
_MAX_LINK = 100


class FAQ(models.Model):
    """
    FAQ table. Stores the pull of answers and questions for FAQ page
    """
    question = models.CharField(editable=False)
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

    rate = models.SmallIntegerField(default=0, db_default=0, blank=True, help_text='Пожалуйста, оцените работу сервиса')
    text = models.TextField(default='', db_default='', help_text='Поделитесь впечатлениями о работе сервиса', blank=True, max_length=_MAX_FEEDBACK)
    reply = models.TextField(default='', db_default='', blank=True, max_length=_MAX_FEEDBACK)
    source_link = models.CharField(default='', db_default='', blank=True, max_length=_MAX_LINK)
    feedback_type = models.SmallIntegerField(default=0, db_default=0, choices=_FEEDBACK_TYPE)
    feedback_source = models.SmallIntegerField(default=0, db_default=0, choices=_FEEDBACK_SOURCE)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=False, db_default=None)

    def __str__(self):
        return self.rate.__str__() + ": " + self.text.__str__()

    class Meta:
        # Lower rates with details first
        # ordering = ['rate', '-text']
        constraints = [
            models.CheckConstraint(check=models.Q(rate__gte=0) | models.Q(text__neq=''), name='empty_feedback')
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

    feedback_source = models.SmallIntegerField(default=2, db_default=2, choices=_USER_GROUP)
    registration_date = models.DateField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=_MAX_NAME)
    second_name = models.CharField(max_length=_MAX_NAME)
    last_name = models.CharField(max_length=_MAX_NAME)
    phone = models.CharField(max_length=_MAX_PHONE, help_text='Основной контактный номер')
    email = models.EmailField(help_text='Действующий адрес электронной почты')
    birthdate = models.DateField(blank=True)
    pref_delivery_type = models.SmallIntegerField(default=0, db_default=0, blank=True, choices=_DELIVERY_TYPE)
    main_address = models.CharField(max_length=_MAX_ADDRESS, blank=True, default='', db_default='')

    def __str__(self):
        return self.name.__str__() + " " + self.second_name.__str__() + " " + self.last_name.__str__()
