# Create your views here.
from allauth.headless.contrib.rest_framework.authentication import (
    XSessionTokenAuthentication,
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import HazardSerializer
from api.models import Hazard


# ViewSets define the view behavior.
class HazardViewset(viewsets.ViewSet):
    authentication_classes = [XSessionTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Hazard.objects.all()
    serializer_class = HazardSerializer
