from rest_framework import serializers
from .models import FinancialData

class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = '__all__'  # Include all fields from the FinancialData model