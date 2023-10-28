from django.conf import settings
from django.db import models
from users.models import NULLABLE
from typing import List, Optional


class Course(models.Model):
    course_name = models.CharField(max_length=200, related_name='subscriptions', verbose_name='Название')
    course_preview = models.ImageField(upload_to='main/course/', verbose_name='Превью', **NULLABLE)
    course_description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=50000, verbose_name='Стоимость курса')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    @classmethod
    def get_all_courses(cls) -> List['Course']:
        return cls.objects.all()

    @classmethod
    def get_by_id(cls, lesson_id: int) -> Optional['Lesson']:
        try:
            return cls.objects.get(id=lesson_id)
        except cls.DoesNotExist:
            return None


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    lesson_name = models.CharField(max_length=200, verbose_name='Название')
    lesson_description = models.TextField(verbose_name='Описание')
    lesson_preview = models.ImageField(upload_to='main/lesson/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

        @classmethod
    def get_all_lessons(cls) -> List['Lesson']:
        return cls.objects.all()

    @classmethod
    def get_by_id(cls, lesson_id: int) -> Optional['Lesson']:

        try:
            return cls.objects.get(id=lesson_id)
        except cls.DoesNotExist:
            return None


class Payment(models.Model):
    METHOD_CHOICES = (
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перевод на счет'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь',
                             **NULLABLE)
    date = models.DateTimeField(verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплата курса')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплата урока')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    method = models.CharField(max_length=40, choices=METHOD_CHOICES, verbose_name='Способ оплаты')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'Платеж от {self.user} на сумму {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    is_subscribed = models.BooleanField(default=False, verbose_name='ok подписки')

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    @classmethod
    def get_all_course_subscriptions(cls) -> List['Lesson']:

        return cls.objects.all()
