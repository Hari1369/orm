from rest_framework import serializers
from .models import api_data, Members

# class api_serializers(serializers.ModelSerializer):
#     employee_id = serializers.PrimaryKeyRelatedField(
#         source='employee',
#         queryset=Members.objects.all()
#     )
#     class Meta:
#         model = api_data
#         fields = '__all__'
class api_serializers(serializers.ModelSerializer):
    class Meta:
        model = api_data
        fields = '__all__'
