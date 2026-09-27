from django.db import models
from django.utils.translation import gettext_lazy as _

class Promotion(models.Model):
    class DiscountTypeChoices(models.TextChoices):
        PERCENT = 'percent', _('Percent')
        FIXED_AMOUNT = 'fixed_amount', _('Fixed Amount')
        BONUS_MULTIPLIER = 'bonus_multiplier', _('Bonus Multiplier')
        FREE_HOUR = 'free_hour', _('Free Hour')

    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='promotions',
        help_text="Оставьте пустым, если акция действует во всех клубах сети"
    )
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    banner = models.URLField(max_length=255, null=True, blank=True, verbose_name=_("Баннер"))

    discount_type = models.CharField(
        max_length=25,
        choices=DiscountTypeChoices.choices,
        verbose_name=_("Тип скидки")
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Размер скидки (процент, сумма в рублях или множитель бонусов)"
    )

    applicable_zone = models.ForeignKey(
        'clubs.Zone',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='promotions',
        help_text="Оставьте пустым, если акция действует для всех зон"
    )

    promo_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        unique=True,
        help_text="Опциональный промокод для активации"
    )

    start_date = models.DateTimeField(verbose_name=_("Дата начала"))
    end_date = models.DateTimeField(verbose_name=_("Дата окончания"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активна"))

    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_promotions',
        verbose_name=_("Кем создана")
    )

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['-start_date']

    def __str__(self):
        status = "Активна" if self.is_active else "Неактивна"
        return f"{self.title} ({self.get_discount_type_display()}) - {status}"
