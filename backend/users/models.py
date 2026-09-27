from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# 1. Менеджер пользователей
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('Номер телефона обязателен для создания пользователя'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', _('Client')
        STAFF = 'staff', _('Staff')
        ADMIN = 'admin', _('Admin')

    # Удаляем стандартное поле username
    username = None

    phone_number = models.CharField(
        _('Номер телефона'),
        max_length=20,
        unique=True
    )
    email = models.EmailField(_('Email'), blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT
    )

    home_club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text="Клуб, в котором зарегистрирован или чаще всего играет клиент"
    )

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [] # Телефон и пароль требуются по умолчанию

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.phone_number} ({self.get_full_name() or self.get_role_display()})"


# 3. Модель профиля сотрудника
class StaffProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        related_name='staff'
    )
    position = models.CharField(
        max_length=100,
        help_text="Например: Администратор зала, Менеджер, Техник"
    )
    hired_at = models.DateField(verbose_name="Дата найма")

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.position} в {self.club.name}"
