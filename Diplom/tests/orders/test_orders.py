import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
    ['is_staff', 'expected_number'],
    (
            (True, 2),
            (False, 1),
    )
)
@pytest.mark.django_db
def test_list_orders(api_client, order_factory, get_token, create_user, is_staff, expected_number):
    test_user = create_user(is_staff=is_staff)
    token = Token.objects.get_or_create(user=test_user)[0].key
    user = create_user()
    order1 = order_factory(user_id_id=user.id)
    order2 = order_factory(user_id_id=test_user.id)
    url = reverse('orders-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert len(resp.json()) == expected_number


@pytest.mark.django_db
def test_unauthorized_list_orders(api_client, order_factory):
    order = order_factory()
    url = reverse('orders-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert order.id


@pytest.mark.django_db
def test_get_order(api_client, order_factory, get_token):
    token = get_token(is_staff=True)
    order = order_factory()
    url = reverse('orders-detail', args=(order.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert resp.json()['id'] == order.id


@pytest.mark.django_db
def test_unauthorized_get_order(api_client, order_factory):
    order = order_factory()
    url = reverse('orders-detail', args=(order.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert order.id


@pytest.mark.parametrize(
    ["quantity", "expected_status"],
    (
            (1, HTTP_201_CREATED),
            (0, HTTP_400_BAD_REQUEST),
            ('', HTTP_400_BAD_REQUEST)
    )
)
@pytest.mark.django_db
def test_create_order(api_client, get_token, product_factory, quantity, expected_status):
    token = get_token()
    product = product_factory()
    url = reverse('orders-list')

    payload = {
        "positions": [
            {
                "product_id": product.id,
                "quantity": quantity
            }
        ]
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == expected_status


@pytest.mark.django_db
def test_create_empty_order(api_client, get_token):
    token = get_token()
    url = reverse('orders-list')

    payload = {
        "positions": []
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_repeat_positions_order(api_client, get_token, product_factory):
    token = get_token()
    product = product_factory()
    url = reverse('orders-list')

    payload = {
        "positions": [
            {
                "product_id": product.id,
                "quantity": 1
            },
            {
                "product_id": product.id,
                "quantity": 1
            }
        ]
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_unauthorized_create_order(api_client, get_token, product_factory):
    product_factory()
    url = reverse('orders-list')

    payload = {
        "positions": [
            {
                "product_id": 1,
                "quantity": 1
            }
        ]
    }

    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    ['is_staff', 'expected_order_status', 'expected_status'],
    (
            (True, "DONE", HTTP_200_OK),
            (False, "NEW", HTTP_403_FORBIDDEN),
    )
)
@pytest.mark.django_db
def test_patch_order(api_client, order_factory, get_token, is_staff, expected_order_status, expected_status):
    order = order_factory()
    token = get_token(is_staff=is_staff)
    url = reverse('orders-detail', args=(order.id,))

    payload = {
        "status": "DONE"
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.patch(url, payload, format='json')
    assert resp.status_code == expected_status
    order.refresh_from_db()
    assert order.status == expected_order_status


@pytest.mark.parametrize(
    ['is_staff', 'expected_status'],
    (
            (True, HTTP_204_NO_CONTENT),
            (False, HTTP_403_FORBIDDEN),
    )
)
@pytest.mark.django_db
def test_destroy_order(api_client, order_factory, get_token, is_staff, expected_status):
    order = order_factory()
    token = get_token(is_staff=is_staff)
    url = reverse('orders-detail', args=(order.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url)
    assert resp.status_code == expected_status
