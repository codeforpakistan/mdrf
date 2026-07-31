from .models import Disaster, Hazard, Location
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