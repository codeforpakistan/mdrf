from django.urls import path

from app.views import disasters, hazards, home, issues, subscriptions, volunteer

urlpatterns = [
    path("", home.index, name="home"),
    path("disasters/", disasters.DisasterListView.as_view(), name="disaster_list"),
    path("disasters/<int:pk>/", disasters.DisasterDetailView.as_view(), name="disaster_detail"),
    path("hazards/", hazards.HazardListView.as_view(), name="hazard_list"),
    path("hazards/<path:hazard_path>/", hazards.HazardDetailView.as_view(), name="hazard_detail"),
    path("issues/", issues.IssueListView.as_view(), name="issue_list"),
    path("issues/<int:pk>/", issues.IssueDetailView.as_view(), name="issue_detail"),
    path("volunteer/", volunteer.volunteer, name="volunteer"),
    path("volunteer/delete/", volunteer.withdraw, name="withdraw"),
    path("subscriptions/", subscriptions.SubscriptionListView.as_view(), name="subscription_list"),
    path("subscriptions/create/", subscriptions.SubscriptionCreateView.as_view(), name="subscription_create"),
    path("subscriptions/<int:pk>/delete/", subscriptions.SubscriptionDeleteView.as_view(), name="subscription_delete"),
]