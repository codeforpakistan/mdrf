from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class TrackedModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(TrackedModel):
    file = models.FileField()
    caption = models.CharField(max_length=100, null=True, blank=True)


# Create your models here.
class Hazard(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        ancestors = self.get_ancestors(include_self=True)
        slug_path = '/'.join([ancestor.slug for ancestor in ancestors if ancestor.slug])
        return reverse('hazard_detail', kwargs={'hazard_path': slug_path})


class Disaster(TrackedModel):
    name = models.CharField(max_length=100)
    description = CKEditor5Field(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    hazards = models.ManyToManyField("Hazard", blank=True)
    locations = TreeManyToManyField("Location", blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    

    def __str__(self):
        return self.name
    

class Location(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    code = models.CharField(max_length=10)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name


class Issue(TrackedModel):
    class StatusChoices(models.TextChoices):
        OPEN = 'Open'
        ACTIVE = 'Active'
        BLOCKED = 'Blocked'
        RESOLVED = 'Resolved'
        CLOSED = 'Closed'
        CANCELLED = 'Cancelled'

    title = models.CharField(max_length=150)
    description = CKEditor5Field(null=True, blank=True)
    disaster = models.ForeignKey(Disaster, null=True, blank=True, on_delete=models.SET_NULL)
    hazard = TreeForeignKey(Hazard, null=True, blank=True, on_delete=models.SET_NULL)
    gallery = models.ManyToManyField(Image, blank=True)
    locations = TreeManyToManyField(Location, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices, default=StatusChoices.OPEN)

    def __str__(self):
        return self.title


class Resource(TrackedModel):
    class TypeChoices(models.TextChoices):
        SHELTER = "Shelter"
        FOOD = "Food"
        WATER = "Water"
        MEDICAL = "Medical"
        OTHER = "Other"

    type = models.CharField(choices=TypeChoices, max_length=100)
    name = models.CharField(max_length=100)
    description = CKEditor5Field(blank=True, null=True)
    gallery = models.ManyToManyField(Image, blank=True)
    locations = TreeManyToManyField(Location, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Alert(TrackedModel):
    hazard = models.ForeignKey(Hazard, null=True, blank=True, on_delete=models.SET_NULL)
    disaster = models.ForeignKey(Disaster, null=True, blank=True, on_delete=models.SET_NULL)
    message = CKEditor5Field()

    class Mata:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(hazard__isnull=False) |
                    models.Q(disaster__isnull=False)
                ),
                name='at_least_one_foreign_key'
            )
        ]
    
    def clean(self):
        super().clean()
        # Enforce validation during form submission and admin saving
        if not (self.hazard or self.disaster):
            raise ValidationError("You must associate this alert with at least one Hazard, or Disaster.")


class Subscription(TrackedModel):
    hazard = models.ForeignKey(Hazard, null=True, blank=True, on_delete=models.SET_NULL)
    disaster = models.ForeignKey(Disaster, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hazard", "user"], name="unique_user_hazard"
            ),
            models.UniqueConstraint(
                fields=["disaster", "user"], name="unique_user_disaster"
            ),
            models.CheckConstraint(
                check=models.Q(disaster__isnull=False) | models.Q(hazard__isnull=False),
                name="exists_disaster_hazard"
            ),
        ]
