from django.core.validators import MinValueValidator
from django.db import models


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)  # todo validate breed
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
