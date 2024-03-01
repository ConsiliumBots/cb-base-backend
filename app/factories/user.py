import factory
from factory.django import DjangoModelFactory
from app.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
