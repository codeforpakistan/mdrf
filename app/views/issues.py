# Create your views here.

from django.views.generic import DetailView, ListView

from app.models import Issue


class IssueListView(ListView):
    model = Issue
    template_name = "app/issues/list.html"
    context_object_name = "issues"

class IssueDetailView(DetailView):
    model = Issue
    template_name = "app/issues/detail.html"
    context_object_name = "issue"
