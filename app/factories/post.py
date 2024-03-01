import factory
from factory.django import DjangoModelFactory
from app.models import Post


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    content = factory.Faker('text')
