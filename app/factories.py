from .models import Disaster, Hazard, Location, Resource, Issue
import factory
import factory.fuzzy


class DisasterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Disaster

    name = factory.Faker("company")

    @factory.post_generation
    def locations(self, create, extracted, **kwargs):
        if not create or extracted:
            return
        else:
            hazard = Hazard.objects.order_by('?')[:1]
            self.hazards.set(hazard)
            
            location = Location.objects.order_by('?')[:1]
            self.locations.set(location)

class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    name = factory.Faker("job")
    type = factory.fuzzy.FuzzyChoice(Resource.TypeChoices)
    description = factory.Faker('text')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')

    @factory.post_generation
    def locations(self, create, extracted, **kwargs):
        if not create or extracted:
            return
        else:
            locations = list(Location.objects.order_by('?').values_list('id', flat=True)[:1])
            self.locations.set(locations)

class IssueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Issue

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    disaster = factory.fuzzy.FuzzyChoice(Disaster.objects.all())
    hazard = factory.fuzzy.FuzzyChoice(Hazard.objects.all())

    @factory.post_generation
    def locations(self, create, extracted, **kwargs):
        if not create or extracted:
            return
        else:
            locations = list(Location.objects.order_by('?').values_list('id', flat=True)[:1])
            self.locations.set(locations)
