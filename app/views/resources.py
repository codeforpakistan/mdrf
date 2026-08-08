# Create your views here.

from django.views.generic import DetailView, ListView

from app.models import Resource


class ResourceListView(ListView):
    model = Resource
    template_name = "app/resources/list.html"
    context_object_name = "resources"


class ResourceDetailView(DetailView):
    model = Resource
    template_name = "app/resources/detail.html"
    context_object_name = "resource"
