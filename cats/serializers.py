from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cats.models import SpyCat
from utils.cats_breeds import get_cats_breeds


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ('id', 'name', 'years_of_experience', 'breed', 'salary')

    def validate_breed(self, value: str):
        breeds = get_cats_breeds()
        if value not in breeds:
            raise ValidationError('Incorrect breed')
        return value
