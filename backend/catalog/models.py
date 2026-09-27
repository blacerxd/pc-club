from django.db import models

# Create your models here.


class Game(models.Model):
	id = models.BigAutoField(primary_key=True, unique=True)
	name = models.CharField(max_length=255, null=False, primary_key=False, unique=False)
	slug = models.SlugField(max_length=100, null=False, unique=True)
	description = models.TextField()
	logo = models.URLField(max_length=255, unique=True, null=True, blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateField()

	def __str__(self):
		return self.name

class WorkstationGame(models.Model):
	workstation = models.ForeignKey('catalog.Workstation', on_delete=models.CASCADE, related_name='games')
	game = models.ForeignKey('catalog.Game', on_delete=models.CASCADE, related_name='workstations')

	class Meta:
		unique_together = ('workstation', 'game')

	def __str__(self):
		return f"{self.workstation.name} - {self.game.name}"
