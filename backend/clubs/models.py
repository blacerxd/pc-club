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

	Club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name=working_hours)
	day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
	open_time = models.TimeField()
	close_time = models.TimeField()
	it_24h = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.get_day_of_week_display()} в {self.club.name}"



