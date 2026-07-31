# Create your views here.

from app.models import Disaster
from django.views.generic import ListView, DetailView
from django.http import JsonResponse


class DisasterListView(ListView):
    model = Disaster
    template_name = "app/disasters/list.html"
    context_object_name = "disasters"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Serialize your points to GeoJSON
        locations = context['disasters'].values('locations__name', 'locations__latitude', 'locations__longitude')
        context['locations'] = list(locations)
        return context

class DisasterDetailView(DetailView):
    model = Disaster
    template_name = "app/disasters/detail.html"
    context_object_name = "disaster"
