# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from app.forms import SubscriptionForm
from app.models import Disaster, Hazard, Subscription


class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = "app/subscriptions/list.html"
    context_object_name = "subscriptions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hazards"] = Hazard.objects.all()
        return context


class SubscriptionCreateView(CreateView):
    model = Subscription
    # fields = ['hazard','user']
    form_class = SubscriptionForm
    template_name = "app/subscriptions/create.html"
    success_url = reverse_lazy('subscriptions')
    success_message = "You are subscribed to alerts for '%(hazards)'"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hazards"] = Hazard.objects.all()
        context["disasters"] = Disaster.objects.all()
        return context

    def form_valid(self, form):
        # Link the logged-in user right before saving
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            # Catch the database unique constraint failure
            form.add_error(None, "You are already subscribed to this hazard.")
            return self.form_invalid(form)


class SubscriptionDeleteView(DeleteView):
    model = Subscription
    success_url = reverse_lazy("subscription_list")
