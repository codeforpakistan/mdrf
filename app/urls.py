from django.urls import path
from django.views.generic import TemplateView

from app.views import (
    disasters,
    hazards,
    home,
    issues,
    resources,
    subscriptions,
    volunteer,
)

urlpatterns = [
    path("", home.index, name="home"),
    path("disasters/", disasters.DisasterListView.as_view(), name="disaster_list"),
    path("disasters/<int:pk>/", disasters.DisasterDetailView.as_view(), name="disaster_detail"),
    path("hazards/", hazards.HazardListView.as_view(), name="hazard_list"),
    path("hazards/<path:hazard_path>/", hazards.HazardDetailView.as_view(), name="hazard_detail"),
    path("issues/", issues.IssueListView.as_view(), name="issue_list"),
    path("issues/<int:pk>/", issues.IssueDetailView.as_view(), name="issue_detail"),
    path("resources/", resources.ResourceListView.as_view(), name="resource_list"),
    path("resources/<int:pk>/", resources.ResourceDetailView.as_view(), name="resource_detail"),
    path("volunteer/", volunteer.volunteer, name="volunteer"),
    path("volunteer/delete/", volunteer.withdraw, name="withdraw"),
    path("subscriptions/", subscriptions.SubscriptionListView.as_view(), name="subscription_list"),
    path("subscriptions/create/", subscriptions.SubscriptionCreateView.as_view(), name="subscription_create"),
    path("subscriptions/<int:pk>/delete/", subscriptions.SubscriptionDeleteView.as_view(), name="subscription_delete"),
    path(
        "firebase-messaging-sw.js",
        TemplateView.as_view(
            template_name="app/firebase-messaging-sw.js", 
            content_type="application/javascript"
        ),
        name="firebase-messaging-sw",
    ),
]