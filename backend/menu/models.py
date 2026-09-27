from django.db import models

# Create your models here.

class MenuCategory(models.Model):
	id = models.BigAutoField(primary_key=True, unique=True)
	name = models.CharField(max_length=255, null=False, primary_key=False, unique=False)
	slug = models.SlugField(max_length=100, null=False, unique=True)
	description = models.TextField()
	is_active = models.BooleanField(default=True)
	created_at = models.DateField()

	def __str__(self):
		return self.name

class MenuItem(models.Model):
	id = models.BigAutoField(primary_key=True, unique=True)
	category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
	name = models.CharField(max_length=255, null=False, primary_key=False, unique=False)
	slug = models.SlugField(max_length=100, null=False, unique=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	is_active = models.BooleanField(default=True)
	created_at = models.DateField()

	def __str__(self):
		return self.name
