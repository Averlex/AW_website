from django.db import models

# Create your models here.


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


class UserFeedback(models.Model):
    """
    User feedback table. Stores user scores, feedback text, as well as feedback sources and administration replies
    """
    # link with user?
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
    text = models.TextField(default='', db_default='', help_text='Поделитесь впечатлениями о работе сервиса', blank=True, max_length=500)
    reply = models.TextField(default='', db_default='', blank=True, max_length=500)
    source_link = models.CharField(default='', db_default='', blank=True, max_length=100)
    feedback_type = models.SmallIntegerField(default=0, db_default=0, choices=_FEEDBACK_TYPE)
    feedback_source = models.SmallIntegerField(default=0, db_default=0, choices=_FEEDBACK_SOURCE)

    def __str__(self):
        return self.rate

    class Meta:
        # Lower rates with details first
        # ordering = ['rate', '-text']
        constraints = [
            models.CheckConstraint(check=models.Q(rate__gte=0) | models.Q(text__neq=''), name='empty_feedback')
        ]


