from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import RangeOperators
from django.db.models import Q, Func
from django.core.exceptions import ValidationError
from core.models import TimeStampedModel
from datetime import timedelta

class TsTzRange(Func):
    """
    Кастомная функция для приведения start_time и end_time к диапазону tstzrange
    в PostgreSQL, что необходимо для работы ExclusionConstraint.
    """
    function = 'tstzrange'
    template = "%(function)s(%(expressions)s, '[)')"


class Booking(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', _('В ожидании')
        CONFIRMED = 'confirmed', _('Подтверждено')
        ACTIVE = 'active', _('Активно')
        COMPLETED = 'completed', _('Завершено')
        CANCELLED = 'cancelled', _('Отменено')
        NO_SHOW = 'no_show', _('Не явился')

    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='bookings',
        verbose_name=_("Пользователь")
    )
    workstation = models.ForeignKey(
        'clubs.Workstation',
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name=_("Рабочее место")
    )
    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name=_("Клуб"),
        help_text=_("Денормализовано для быстрых выборок")
    )
    
    start_time = models.DateTimeField(db_index=True, verbose_name=_("Время начала"))
    end_time = models.DateTimeField(db_index=True, verbose_name=_("Время окончания"))

    actual_start = models.DateTimeField(null=True, blank=True, verbose_name=_("Факт заезда"))
    actual_end = models.DateTimeField(null=True, blank=True, verbose_name=_("Факт выезда"))

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        db_index=True,
        verbose_name=_("Статус")
    )

    participants_count = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Количество участников"),
        help_text=_("Для групповых броней bootcamp-зоны")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Стоимость")
    )
    comment = models.TextField(blank=True, verbose_name=_("Комментарий"))

    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_bookings',
        verbose_name=_("Кем создано"),
        help_text=_("Сам пользователь или сотрудник клуба")
    )

    class Meta:
        verbose_name = _("Бронирование")
        verbose_name_plural = _("Бронирования")
        # Ограничение целостности на уровне БД против двойного бронирования
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_bookings',
                expressions=[
                    ('workstation', RangeOperators.EQUAL),
                    (TsTzRange('start_time', 'end_time'), RangeOperators.OVERLAPS),
                ],
                condition=Q(status__in=['pending', 'confirmed', 'active']),
            )
        ]

    def clean(self):
        super().clean()
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(_("Время начала должно быть раньше времени окончания."))
            
            # ВАРИАНТ 1: Буферное время 15 минут между сеансами
            buffer_time = timedelta(minutes=15)
            
            qs = Booking.objects.filter(
                workstation=self.workstation,
                status__in=[self.StatusChoices.PENDING, self.StatusChoices.CONFIRMED, self.StatusChoices.ACTIVE]
            )
            # Исключаем текущую бронь из проверки (если это редактирование)
            if self.pk:
                qs = qs.exclude(pk=self.pk)

            # Ищем пересечения с учетом буфера:
            # (Конец другой брони + 15м) задевает (Начало нашей брони)
            # И (Начало другой брони - 15м) задевает (Конец нашей брони)
            overlapping = qs.filter(
                end_time__gt=self.start_time - buffer_time,
                start_time__lt=self.end_time + buffer_time
            )

            if overlapping.exists():
                raise ValidationError({
                    'start_time': _("Между сеансами должен быть перерыв минимум 15 минут для уборки и возможности продления.")
                })

    def __str__(self):
        return f"Бронь #{self.pk} - {self.workstation} ({self.start_time.strftime('%d.%m %H:%M')})"


class BookingStatusLog(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='status_logs',
        verbose_name=_("Бронирование")
    )
    old_status = models.CharField(
        max_length=20,
        choices=Booking.StatusChoices.choices,
        null=True,
        blank=True,
        verbose_name=_("Старый статус")
    )
    new_status = models.CharField(
        max_length=20,
        choices=Booking.StatusChoices.choices,
        verbose_name=_("Новый статус")
    )
    changed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booking_status_changes',
        verbose_name=_("Кем изменено")
    )
    comment = models.TextField(blank=True, verbose_name=_("Комментарий"))
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Время изменения"))

    class Meta:
        verbose_name = _("Лог статуса бронирования")
        verbose_name_plural = _("Логи статусов бронирования")
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.booking} | {self.old_status} -> {self.new_status}"


class Waitlist(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        WAITING = 'waiting', _('В очереди')
        NOTIFIED = 'notified', _('Оповещен')
        BOOKED = 'booked', _('Забронировано')
        EXPIRED = 'expired', _('Истекло')
        CANCELLED = 'cancelled', _('Отменено')

    # Дублируем DEVICE_CHOICES из Workstation для независимости, 
    # либо можно импортировать, но лучше явно определить
    class DeviceTypeChoices(models.TextChoices):
        PC = 'PC', _('ПК')
        PS5 = 'PS5', _('PlayStation 5')
        XBOX = 'XBOX', _('Xbox Series X/S')

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='waitlist_entries',
        verbose_name=_("Пользователь")
    )
    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        related_name='waitlist_entries',
        verbose_name=_("Клуб")
    )
    zone = models.ForeignKey(
        'clubs.Zone',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='waitlist_entries',
        verbose_name=_("Зона"),
        help_text=_("Если ждет место в конкретной зоне")
    )
    device_type = models.CharField(
        max_length=10,
        choices=DeviceTypeChoices.choices,
        null=True,
        blank=True,
        verbose_name=_("Тип устройства"),
        help_text=_("Если ждет любую консоль/ПК определённого типа")
    )
    desired_start = models.DateTimeField(verbose_name=_("Желаемое время начала"))
    desired_duration = models.DurationField(verbose_name=_("Желаемая длительность"))
    
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.WAITING,
        verbose_name=_("Статус")
    )
    notified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Когда оповещен")
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Срок действия оповещения")
    )

    class Meta:
        verbose_name = _("Запись в листе ожидания")
        verbose_name_plural = _("Листы ожидания")
        ordering = ['created_at']

    def __str__(self):
        target = self.zone.name if self.zone else self.get_device_type_display()
        return f"Очередь: {self.user} -> {target} ({self.get_status_display()})"
