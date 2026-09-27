from django.db import models
from django.utils.translation import gettext_lazy as _

class LoyaltyAccount(models.Model):
    class TierChoices(models.TextChoices):
        BRONZE = 'bronze', _('Bronze')
        SILVER = 'silver', _('Silver')
        GOLD = 'gold', _('Gold')

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='loyalty_account'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tier = models.CharField(
        max_length=15,
        choices=TierChoices.choices,
        null=True,
        blank=True,
        help_text="Опциональный уровень лояльности"
    )

    total_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Аккаунт лояльности"
        verbose_name_plural = "Аккаунты лояльности"

    def __str__(self):
        return f"Баланс {self.user.get_full_name() or self.user.phone_number}: {self.balance}"


class LoyaltyTransaction(models.Model):
    class TypeChoices(models.TextChoices):
        EARN_BOOKING = 'earn_booking', _('Earned from Booking')
        EARN_ORDER = 'earn_order', _('Earned from Order')
        SPEND = 'spend', _('Spent')
        MANUAL_ADMIN = 'manual_admin', _('Manual Admin Entry')
        REFERRAL = 'referral', _('Referral Bonus')

    account = models.ForeignKey(
        LoyaltyAccount,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Сумма начисления (может быть отрицательной при списании)"
    )
    type = models.CharField(max_length=20, choices=TypeChoices.choices)

    # Связи с источниками начисления (могут быть пустыми, если это ручное или реферальное начисление)
    related_booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loyalty_transactions'
    )
    related_order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loyalty_transactions'
    )

    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_loyalty_transactions',
        help_text="Сотрудник, который провел ручное начисление/списание"
    )

    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Транзакция лояльности"
        verbose_name_plural = "Транзакции лояльности"
        ordering = ['-created_at']

    def __str__(self):
        sign = "+" if self.amount > 0 else ""
        return f"{self.account.user.phone_number}: {sign}{self.amount} ({self.get_type_display()})"


class LoyaltyRule(models.Model):
    class ActionTypeChoices(models.TextChoices):
        BOOKING = 'booking', _('Booking')
        ORDER = 'order', _('Order')

    action_type = models.CharField(
        max_length=20,
        choices=ActionTypeChoices.choices,
        unique=True,
        help_text="Тип действия, за которое начисляются баллы"
    )
    points_per_unit = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        help_text="Коэффициент начисления. Например, 0.1 означает 1 балл за каждые 10 ₽"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Правило лояльности"
        verbose_name_plural = "Правила лояльности"

    def __str__(self):
        status = "Активно" if self.is_active else "Неактивно"
        return f"Правило для {self.get_action_type_display()} (Коэфф: {self.points_per_unit}) - {status}"
