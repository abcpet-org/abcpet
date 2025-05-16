from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user', 'address_line1', 'address_line2', 'city', 'state', 
            'postal_code', 'country', 'profile_picture', 'phone_number', 
            'data_sharing_enabled', 'service_related_settings'
        ]