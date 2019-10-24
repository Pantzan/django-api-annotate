import collections
from rest_framework import serializers
from .models import Metric

# dynamic serializer to pass fields only. It removes the remainded fields from the pool
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    cpi = serializers.FloatField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class MetricSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'

    # pass the annotated new fields into the context and present
    def to_representation(self, obj):
        context = super(MetricSerializer, self).to_representation(obj)
        if isinstance(obj, dict):
            for field in set(obj.keys()):
                value = obj.get(field, None)
                if  field.endswith("_") and value is not None:
                    context[field[:-1]] = value
        return context
