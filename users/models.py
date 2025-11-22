from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """класс, определяющий пользователя приложения"""

    username = models.CharField(max_length=50, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15, verbose_name="Телефон", blank=True, null=True
    )
    country = models.CharField(
        max_length=50, verbose_name="Страна", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="images/",
        default="images/placeholder.png",
        verbose_name="Аватар",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = [
            "email",
        ]
        permissions = [
            ("can_blocked_user", "Can blocked user"),
        ]

    def __str__(self):
        return self.email
