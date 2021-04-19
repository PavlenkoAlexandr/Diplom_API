import pytest
from model_bakery import baker
from rest_framework.authtoken.models import Token


@pytest.fixture
def reviews_factory():
    def factory(**kwargs):
        return baker.make("Review", **kwargs)
    return factory
