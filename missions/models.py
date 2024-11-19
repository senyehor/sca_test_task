from django.core.exceptions import ValidationError
from django.db import models


class Target(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_complete = models.BooleanField(default=False)
    mission = models.ForeignKey(
        'missions.Mission',
        on_delete=models.RESTRICT,
        related_name='targets'
    )


class TargetNote(models.Model):
    target = models.ForeignKey(
        'missions.Target',
        on_delete=models.RESTRICT,
        related_name='notes'
    )
    topic = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)


class Mission(models.Model):
    cat = models.ForeignKey(
        'cats.SpyCat',
        null=True,
        on_delete=models.RESTRICT,
        related_name='missions'
    )
    is_complete = models.BooleanField(default=False)

    MIN_TARGET_COUNT = 1
    MAX_TARGET_COUNT = 3

    def delete(self, using=None, keep_parents=False):
        if self.cat:
            raise ValidationError('Cannot delete a mission that is assigned to a cat')
        return super().delete(using, keep_parents)
