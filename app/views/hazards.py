# Create your views here.

import os
from typing import Any

from django.conf import settings
from django.db.models import F
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from app.models import Hazard


class HazardListView(ListView):
    model = Hazard
    template_name = "app/hazards/list.html"
    context_object_name = "hazards"

    def get_queryset(self) -> QuerySet[Any, Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(is_visible=True)
        return queryset

    # def setup(self, request, *args, **kwargs):
    #     """Extract path arguments early to use across multiple methods."""
    #     super().setup(request, *args, **kwargs)
    #     # Split path string and fetch the last slug item
    #     slug_list = [s for s in self.kwargs.get('hazard_path', '').split('/') if s]
    #     leaf_slug = slug_list[-1] if slug_list else None
        
    #     # Look up the category record
    #     self.hazard = get_object_or_404(Hazard, slug=leaf_slug)

    # def get_queryset(self) -> QuerySet[Any, Any]:
    #     """Return items belonging to this category and all its subcategories."""
    #     # Use MPTT's get_descendants to include nested child items automatically
    #     hazards = self.hazard.get_descendants(include_self=True)
    #     return Hazard.objects.filter(hazard__in=hazards).select_related('hazard')

    # def get_context_data(self, **kwargs):
    #     """Inject the current category object into the template context."""
    #     context = super().get_context_data(**kwargs)
    #     context['hazard'] = self.hazard
    #     return context
    
    
class HazardDetailView(DetailView):
    model = Hazard
    template_name = "app/hazards/detail.html"
    context_object_name = "hazard"

    def get_object(self, queryset=None):
        """Manually parse the custom path parameter to fetch the object."""
        # 1. Get the path string from URLconf kwargs
        hazard_path = self.kwargs.get('hazard_path', '')
        
        # 2. Extract the last slug element
        slug_list = [s for s in hazard_path.split('/') if s]
        leaf_slug = slug_list[-1]
        
        # 3. Use the preferred queryset or the default manager
        if queryset is None:
            queryset = self.get_queryset()
            
        # 4. Fetch the unique leaf node record
        return get_object_or_404(queryset, slug=leaf_slug)

    def get_template_names(self):
        slug = self.kwargs.get("slug")
        template_name = f"app/hazards/{slug}.html"
        file_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], template_name)
        if os.path.exists(file_path):
            return [template_name]
        return ["app/hazards/detail.html"]
