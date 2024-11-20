from django.db.models import Model
from django.db.transaction import atomic
from django.utils.decorators import method_decorator
from rest_framework.exceptions import ValidationError


class UpdatableFieldsModelSerializerMixin:
    @method_decorator(atomic)
    def update(self, instance: Model, validated_data: dict):
        self.__check_validated_data_has_only_updatable_fields(validated_data)
        instance = self.__perform_update(instance, validated_data)
        return instance

    def __perform_update(self, instance: Model, validated_data: dict):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def __check_validated_data_has_only_updatable_fields(self, validated_data: dict):
        validated_fields = set(validated_data.keys())
        updatable_fields = set(self.Meta.updatable_fields)  # noqa
        invalid_fields = validated_fields - updatable_fields
        if invalid_fields:
            raise ValidationError(
                f"The following fields cannot be updated: {list(invalid_fields)}. "
                f"Only these fields can be updated: {list(updatable_fields)}"
            )
