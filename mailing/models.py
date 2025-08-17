from django.db import models
from users.models import CustomUser

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
    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_FINISHED = 'finished'
    STATUS_CHOICES = [
                      (STATUS_CREATED, 'Создана'),
                      (STATUS_STARTED, 'Запущена'),
                      (STATUS_FINISHED, 'Завершена'),
                     ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    finished_at = models.DateTimeField(auto_now=True, verbose_name='Дата завершения')
    is_active = models.BooleanField(default=False, verbose_name='Активная')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение', blank=True)
    recipients = models.ManyToManyField(Recipient, related_name='mailings', verbose_name='Получатели')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mailings', verbose_name='Владелец', blank=True, null=True)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['pk']
        db_table = 'mailings'

    def __str__(self):
        return f"Рассылка {self.pk} - {self.status}"
