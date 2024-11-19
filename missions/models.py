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
    author = models.ForeignKey(
        'cats.SpyCat',
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

    def clean(self):
        self.__check_more_than_one_less_than_three_targets()

    def __check_more_than_one_less_than_three_targets(self):
        if not (1 <= self.targets.count() <= 3):
            raise ValidationError('A mission must have between 1 and 3 targets.')

    def __check_cat_has_no_other_mission(self):
        if self.cat is None:
            return
        if Mission.objects.filter(cat=self.cat).exclude(id=self.id).exists():
            raise ValidationError('The cat is already assigned a mission')

    def delete(self, using=None, keep_parents=False):
        if self.cat:
            raise ValidationError('Cannot delete a mission that is assigned to a cat')
        return super().delete(using, keep_parents)