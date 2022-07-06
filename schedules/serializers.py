from rest_framework import serializers

from .models import Schedule


# Create a SCHEDULE serializer
class ScheduleSerializer(serializers.ModelSerializer):
    # specify model and fields
    # these fields will be serialized
    class Meta:
        model = Schedule
        fields = '__all__'

    # checking for negative dates exception handling
    def validate(self, data):
        if 1 > data['birth_date'] > 31:
            raise serializers.ValidationError({'error': 'date cant be negative or 0'})
        if 1 > data['birth_month'] > 12:
            raise serializers.ValidationError({'error': 'month cant be negative or 0'})

        # else no exception is raised just pass data
        return data
