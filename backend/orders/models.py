from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

class Order(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        NEW = 'new', _('Новый')
        ACCEPTED = 'accepted', _('Принят')
        COOKING = 'cooking', _('Готовится')
        DELIVERED = 'delivered', _('Доставлен')
        CANCELLED = 'cancelled', _('Отменен')

    class PaymentMethodChoices(models.TextChoices):
        BONUS = 'bonus', _('Бонусы')
        CASH = 'cash', _('Наличные')
        CARD = 'card', _('Карта')

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_("Пользователь")
    )
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name=_("Привязка к сессии (брони)")
    )
    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_("Клуб")
    )
    
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
        verbose_name=_("Статус заказа")
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Общая стоимость")
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoices.choices,
        verbose_name=_("Способ оплаты")
    )
    comment = models.TextField(blank=True, verbose_name=_("Комментарий к заказу"))
    
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Время доставки"))

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user} ({self.get_status_display()})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_("Заказ")
    )
    menu_item = models.ForeignKey(
        'menu.MenuItem',
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_("Позиция меню")
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Количество"))
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Цена на момент заказа"),
        help_text=_("Фиксирует цену товара, чтобы она не изменилась в истории при смене цены в меню")
    )

    class Meta:
        verbose_name = _("Позиция заказа")
        verbose_name_plural = _("Позиции заказа")

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Заказ #{self.order.pk})"
