from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Hazard


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class HazardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hazard
        fields = "__all__"
