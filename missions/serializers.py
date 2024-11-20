from django.db.transaction import atomic
from django.utils.decorators import method_decorator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cats.models import SpyCat
from missions.models import Mission, Target, TargetNote


class TargetNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetNote
        fields = ['id', 'target', 'topic', 'content']


class TargetSerializer(serializers.ModelSerializer):
    notes = TargetNoteSerializer(many=True, required=False)

    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'is_complete', 'notes']


class MissionSerializer(serializers.ModelSerializer):
    cat = serializers.PrimaryKeyRelatedField(
        queryset=SpyCat.objects.all(),
        required=False
    )
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ('id', 'cat', 'is_complete', 'targets')
        updatable_fields = ('cat', 'is_complete')

    @method_decorator(atomic)
    def create(self, validated_data: dict):
        targets_data = validated_data.pop('targets')
        if validated_data.get('is_complete', None) is True:
            raise ValidationError('Cannot create a completed mission')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            # todo refuse with notes
            Target.objects.create(mission=mission, **target_data)
        return mission

    @method_decorator(atomic)
    def update(self, instance: Mission, validated_data: dict):
        self.__check_mission_is_not_complete(instance)
        self.__check_validated_data_has_only_updatable_fields(validated_data)
        mission = self.__perform_update(instance)
        return mission

    def __perform_update(self, mission: Mission, validated_data: dict):
        for field, value in validated_data.items():
            setattr(mission, field, value)
        mission.save()
        return mission

    def __check_mission_is_not_complete(self, mission: Mission):
        if mission.is_complete:
            raise ValidationError('Cannot update completed mission')

    def __check_validated_data_has_only_updatable_fields(self, validated_data: dict):
        validated_fields = set(validated_data.keys())
        updatable_fields = set(self.Meta.updatable_fields)
        invalid_fields = validated_fields - updatable_fields
        if invalid_fields:
            raise ValidationError(
                f"The following fields cannot be updated: {list(invalid_fields)}. "
                f"Only these fields can be updated: {list(updatable_fields)}"
            )

    def validate_cat(self, value):
        if mission_id := self.initial_data.get('id', None):
            if Mission.objects.filter(cat_id=value).exclude(id=mission_id).exists():
                raise ValidationError('The cat is already assigned a mission')
        return value

    def validate_targets(self, value):
        if not (Mission.MIN_TARGET_COUNT <= len(value) <= Mission.MAX_TARGET_COUNT):
            raise ValidationError('A mission must have between 1 and 3 targets')
        return value
