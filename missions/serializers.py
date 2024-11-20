from django.db.transaction import atomic
from django.utils.decorators import method_decorator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cats.models import SpyCat
from missions.models import Mission, Target, TargetNote
from utils.updatable_fields_model_serializer_mixin import UpdatableFieldsModelSerializerMixin


class TargetNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetNote
        fields = ['id', 'target', 'topic', 'content']


class TargetSerializer(UpdatableFieldsModelSerializerMixin, serializers.ModelSerializer):
    notes = TargetNoteSerializer(many=True, required=False)

    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'is_complete', 'notes']
        updatable_fields = ('is_complete',)


class MissionSerializer(UpdatableFieldsModelSerializerMixin, serializers.ModelSerializer):
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

    def validate_cat(self, value):
        # check whether we work with already existing mission
        if self.instance:
            if Mission.objects.filter(cat_id=value).exclude(id=self.instance.id).exists():
                raise ValidationError('The cat is already assigned a mission')
        return value

    def validate_targets(self, value):
        if not (Mission.MIN_TARGET_COUNT <= len(value) <= Mission.MAX_TARGET_COUNT):
            raise ValidationError('A mission must have between 1 and 3 targets')
        return value
