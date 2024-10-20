from rest_framework.serializers import ModelSerializer

from users.models import User, Donation


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DonationSerializer(ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
