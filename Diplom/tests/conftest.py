import pytest
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        user = baker.make(django_user_model, **kwargs)
        return user
    return make_user


@pytest.fixture
def get_token(db, create_user):
    def _get_token(is_staff=False):
        user = create_user(is_staff=is_staff)
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
    return _get_token


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make("Product", **kwargs)
    return factory


@pytest.fixture()
def user_for_test(create_user):
    user = create_user()
    token = Token.objects.get_or_create(user=user)[0].key
    return {'user': user, 'token': token}
