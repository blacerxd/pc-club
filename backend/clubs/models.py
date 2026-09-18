from django.db import models

# Create your models here.

class Club(models.Model):
	id = models.BigAutoField(primary_key=True, unique=True)
	name = models.CharField(max_length=255, null=False, primary_key=False, unique=False)
	slug = models.SlugField(max_length=100, null=False, unique=True)
	adress = models.CharField(max_length=255, null=False)
	city = models.CharField(max_length=255, null=False)
	latitude = models.CharField(max_length=50, unique=True)
	longitude = models.CharField(max_length=50, unique=True)
	phone = models.CharField(max_length=25, unique=True, null=False)
	email = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	logo = models.URLField(max_length=255, unique=True, null=True, blank=True)
	photos = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	created_at = models.DateField()

	def __str__(self):
		return self.name

class ClubWorkingHours(models.Model):
	DAYS_OF_WEEK = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ]

	club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name=working_hours)
	day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
	open_time = models.TimeField()
	close_time = models.TimeField()
	it_24h = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.get_day_of_week_display()} в {self.club.name}"

class Zone(models.Model):
	ZONE_CHOICES = [
        ('STANDARD', 'Standard'),
        ('VIP', 'VIP Room'),
        ('BOOTCAMP', 'Bootcamp'),
    ]
	id = models.BigAutoField(primary_key=True, unique=True)
	club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name=Zone)
	name = models.CharField(max_length=255)
	zone_type = models.CharField(max_length=25, choices=ZONE_CHOICES, default='STANDART')
	description = models.CharField(max_length=255, blank=True)
	capacity = models.PositiveIntegerField(help_text="Количество мест в зоне")
	color = models.CharField(max_length=7, default='#FFFFFF', help_text="hex-код цвета")
	icon = models.CharField(max_length=50, blank=True, null=True, help_text="Имя иконки для фронтенда")

class ZonePriceModifier(models.Model):
    DAYS_CHOICES = [
        ('WEEKDAYS', 'Будни (Пн-Пт)'),
        ('WEEKENDS', 'Выходные (Сб-Вс)'),
    ]

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='price_modifiers')
    day_type = models.CharField(max_length=10, choices=DAYS_CHOICES)

    # Временной интервал действия этой цены
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Конкретная цена, которая заменит базовую в этот промежуток времени
    special_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Цена для {self.zone.name} в {self.get_day_type_display()} ({self.start_time}-{self.end_time})"

class Peripheral(models.Model):
    TYPE_CHOICES = [
        ('MOUSE', 'Мышь'),
        ('KEYBOARD', 'Клавиатура'),
        ('HEADSET', 'Гарнитура'),
        ('MONITOR', 'Монитор'),
        ('CHAIR', 'Кресло'),
    ]

    brand = models.CharField(max_length=50, help_text="Например: Logitech, Razer")
    model_name = models.CharField(max_length=100, help_text="Например: G Pro X Superlight")
    device_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    specs = models.TextField(blank=True, null=True, help_text="Например: 25600 DPI, беспроводная")

    class Meta:
        verbose_name = "Девайс"
        verbose_name = "Девайсы"
        # Защита от дубликатов: нельзя создать два одинаковых девайса одного бренда
        unique_together = ('brand', 'model_name')

    def __str__(self):
        return f"{self.get_device_type_display()}: {self.brand} {self.model_name}"

class HardwareProfile(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=255)
	cpu = models.CharField(max_length=255)
	gpu = models.CharField(max_length=255)
	ram = models.CharField(max_length=255)
	monitor = models.CharField(max_length=255)
	monitor_refresh_rate = models.CharField(max_length=255)
	peripherals = models.ManyToManyField(
        Peripheral,
        related_name='zones',
        blank=True,
        help_text="Выберите девайсы, установленные в этой зоне"
    )
	def __str__(self):
		return f"{self.name} в {self.club.name}"

class Workstaion(models.Model):
	DEVICE_CHOICES = [
        ('PC', 'ПК'),
        ('PS5', 'PlayStation 5'),
        ('XBOX', 'Xbox Series X/S'),
    ]
	STATUS_CHOICES = [
        ('FREE', 'Свободно'),
        ('OCCUPIED', 'Занято'),
        ('RESERVED', 'Забронировано'),
        ('MAINTENANCE', 'Тех. обслуживание'),
    ]
	zone = models.ForeignKey(
        'Zone',  # Имя модели строкой, если она объявлена ниже в файле
        on_delete=models.CASCADE,
        related_name='workstations'
    )
	number_label = models.CharField(max_length=20, help_text="Например: PC-12, PS5-02")
	device_type = models.CharField(max_length=10, choices=DEVICE_CHOICES, default='PC')
	hardware_profile = models.ForeignKey(
        HardwareProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='workstations'
    )

	status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='FREE')

    # Координаты для интерактивной карты зала на фронтенде
    # Позволяют перетаскивать и позиционировать ПК в админке
	position_x = models.IntegerField(blank=True, null=True, help_text="X-координата (в пикселях или процентах)")
	position_y = models.IntegerField(blank=True, null=True, help_text="Y-координата (в пикселях или процентах)")

	class Meta:
		verbose_name = "Рабочее место"
		verbose_name = "Рабочие места"

		unique_together = ('zone', 'number_label')

	def __str__(self):
		return f"{self.number_label} ({self.get_device_type_display()}) — {self.zone.name}"


