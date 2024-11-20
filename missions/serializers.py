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

    @method_decorator(atomic)
    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            # todo refuse with notes
            Target.objects.create(mission=mission, **target_data)
        return mission

    @method_decorator(atomic)
    def update(self, instance, validated_data):
        targets_data = validated_data.pop('targets', [])
        instance = self.__update_instance(instance, validated_data)
        self.__update_or_create_targets(instance, targets_data)
        return instance

    def validate_cat(self, value):
        if mission_id := self.initial_data.get('id', None):
            if Mission.objects.filter(cat_id=value).exclude(id=mission_id).exists():
                raise ValidationError('The cat is already assigned a mission')
        return value

    def validate_targets(self, value):
        if not (Mission.MIN_TARGET_COUNT <= len(value) <= Mission.MAX_TARGET_COUNT):
            raise ValidationError('A mission must have between 1 and 3 targets')
        return value

    def __update_instance(self, instance: Mission, validated_data) -> Mission:
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def __update_or_create_targets(self, mission: Mission, targets_data):
        for target_data in targets_data:
            if target_id := target_data.get('id'):
                target = Target.objects.get(id=target_id, mission=mission)
                self.__update_target(target, target_data)
            else:
                if 'notes' in target_data:
                    raise ValidationError('Target cannot be created along with notes')
                Target.objects.create(mission=mission, **target_data)

    def __update_target(self, target: Target, update_data):
        if target.is_complete:
            raise ValidationError('Cannot update completed target')
        notes_data = update_data.pop('notes', [])
        # todo catch exceptions
        for field, value in update_data.items():
            setattr(target, field, value)
        target.save()
        if notes_data:
            self.__update_notes(target, notes_data)

    def __update_notes(self, target: Target, notes_data):
        for note_data in notes_data:
            if note_id := note_data.get('id'):
                # todo catch exceptions
                TargetNote.objects.filter(id=note_id).update(**note_data)
            else:
                TargetNote.objects.create(target=target, **note_data)
