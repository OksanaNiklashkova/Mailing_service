from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Recipient(models.Model):
    """Модель для создания получателя рассылки"""
    email = models.EmailField(unique=True, verbose_name='Адрес получателя')
    recipient_name = models.CharField(max_length=100, default='клиент', blank=True, null= True, verbose_name='ФИО получателя')
    comment = models.TextField(max_length=150, default='', blank=True, null= True, verbose_name='Комментарий')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipients', verbose_name='Владелец', blank=True)

    def __str__(self):
        return f'Клиент - {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['email', ]
        db_table = 'recipients'


class Message(models.Model):
    """Модель для создания сообщения"""
    topik = models.CharField(max_length=150, default='Без темы', blank=True, null= True, verbose_name='Тема сообщения')
    text = models.TextField(default='', blank=True, null= True, verbose_name='Текст сообщения')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages', verbose_name='Владелец', blank=True)

    def __str__(self):
        return f'Сообщение: {self.topik}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['topik', ]
        db_table = 'messages'


class Mailing(models.Model):
    """Модель для создания рассылок"""
    STATUS_CREATED = 'создана'
    STATUS_STARTED = 'запущена'
    STATUS_FINISHED = 'завершена'
    STATUS_CHOICES = [
                      (STATUS_CREATED, 'создана'),
                      (STATUS_STARTED, 'запущена'),
                      (STATUS_FINISHED, 'завершена'),
                     ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    started_at = models.DateTimeField(blank=True, null=True, verbose_name='Начало рассылки')
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name='Завершение рассылки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение', blank=True)
    recipients = models.ManyToManyField(Recipient, related_name='mailings', verbose_name='Получатели')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mailings', verbose_name='Владелец', blank=True, null=True)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['pk']
        db_table = 'mailings'
        permissions = [
            ('can_finished_mailing', 'Can finished mailing'),
        ]

    def __str__(self):
        return f"Рассылка {self.pk} от пользователя {self.owner} - {self.status}"


class SendAttempt(models.Model):
    """Модель попытки рассылки"""
    STATUS_SUCCESS = 'успешно'
    STATUS_UNSUCCES = 'не успешно'
    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'успешно'),
        (STATUS_UNSUCCES, 'не успешно'),
    ]

    attempt_datetime = models.DateTimeField(default=timezone.now, verbose_name='Дата попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_UNSUCCES, verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ сервера')
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='send_attempts', verbose_name='Рассылка')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='send_attempts', verbose_name='Владелец',
                              blank=True, null=True)

    def __str__(self):
        return f"Попытка для рассылки {self.mailing} от пользователя {self.owner} — {self.status} ({self.attempt_datetime})"

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
        ordering = ['status', 'attempt_datetime']
        db_table = 'send_attempts'