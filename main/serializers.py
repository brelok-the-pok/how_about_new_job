from .models import Vacancy

from rest_framework import serializers


class VacancySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(VacancySerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Vacancy
        fields = '__all__'

    def create(self, validated_data):
        """ Create cart if not created """
        defaults = {key: value for key, value in validated_data.items() if key != 'rpc'}
        vacancy, created = Vacancy.objects.update_or_create(
            rpc=validated_data.get('rpc'),
            defaults=defaults
        )
        return vacancy
