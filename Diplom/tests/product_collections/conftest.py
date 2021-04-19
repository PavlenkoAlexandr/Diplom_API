import pytest
from model_bakery import baker


@pytest.fixture
def collection_factory():
    def factory(**kwargs):
        return baker.make('Collection', **kwargs)
    return factory
