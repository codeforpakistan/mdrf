from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from mptt.admin import MPTTModelAdmin

from .models import (
    Alert,
    Disaster,
    Hazard,
    Image,
    Issue,
    Location,
    Resource,
    Subscription,
)

# Register your models here.

@admin.register(Hazard)
class HazardAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug', 'is_visible')
    list_editable = ('is_visible',)
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Disaster)
class DisasterAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        # Check if the user clicked the standard "Save" button
        if "_save" in request.POST:
            # Redirect to a custom named URL pattern
            return HttpResponseRedirect(reverse('disaster_detail', kwargs={ 'pk': obj.id }))
        
        # Fallback to default behavior (e.g., "Save and continue editing")
        return super().response_change(request, obj)

@admin.register(Location)
class LocationAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'disaster', 'hazard']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title','user','status', 'created_at')

    def response_change(self, request, obj):
            # Check if the user clicked the standard "Save" button
            if "_save" in request.POST:
                # Redirect to a custom named URL pattern
                return HttpResponseRedirect(reverse('issue_detail', kwargs={ 'pk': obj.id }))
            
            # Fallback to default behavior (e.g., "Save and continue editing")
            return super().response_change(request, obj)
