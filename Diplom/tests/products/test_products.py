import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_products_list(api_client, product_factory):
    url = reverse('products-list')
    product = product_factory()
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert len(resp.json()) == 1


@pytest.mark.django_db
def test_get_product(api_client, product_factory):
    product = product_factory()
    url = reverse('products-detail', args=(product.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert resp.json()['id'] == product.id


@pytest.mark.parametrize(
    ['is_staff', 'price', 'expected_status'],
    (
            (True, 1, HTTP_201_CREATED),
            (True, -1, HTTP_400_BAD_REQUEST),
            (False, 1, HTTP_403_FORBIDDEN),
    )
)
@pytest.mark.django_db
def test_create_product(api_client, get_token, product_factory, is_staff, price, expected_status):

    token = get_token(is_staff=is_staff)
    url = reverse('products-list')
    payload = {
      "name": "Шоколад",
      "description": "Супер-пупер Шокохруст!",
      "price": price
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    ['is_staff', 'price', 'expected_status'],
    (
            (True, 1, HTTP_200_OK),
            (True, -1, HTTP_400_BAD_REQUEST),
            (False, 1, HTTP_403_FORBIDDEN),
    )
)
@pytest.mark.django_db
def test_update_product(api_client, get_token, product_factory, is_staff, price, expected_status):

    token = get_token(is_staff=is_staff)
    product = product_factory()
    url = reverse('products-detail', args=(product.id,))
    payload = {
        "price": price
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.patch(url, payload, format='json')

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    ['is_staff', 'expected_status'],
    (
            (False, HTTP_403_FORBIDDEN),
            (True, HTTP_204_NO_CONTENT),
    )
)
@pytest.mark.django_db
def test_destroy_product(api_client, get_token, product_factory, is_staff, expected_status):

    token = get_token(is_staff=is_staff)
    product = product_factory()
    url = reverse('products-detail', args=(product.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url)

    assert resp.status_code == expected_status
