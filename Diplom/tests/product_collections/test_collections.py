import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_collections_list(api_client, collection_factory):
    url = reverse('product-collections-list')
    collection = collection_factory()
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert len(resp.json()) == 1


@pytest.mark.django_db
def test_get_collection(api_client, collection_factory):
    collection = collection_factory()
    url = reverse('product-collections-detail', args=(collection.id, ))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert resp.json()['id'] == collection.id


@pytest.mark.parametrize(
    ['is_staff', 'expected_status'],
    (
        (True, HTTP_201_CREATED),
        (False, HTTP_403_FORBIDDEN)
    )
)
@pytest.mark.django_db
def test_create_collection(api_client, product_factory, get_token, is_staff, expected_status):
    token = get_token(is_staff=is_staff)
    url = reverse('product-collections-list')
    product = product_factory()

    payload = {
        "title": "Тест",
        "positions": [
            {
                "product_id": product.id,
                "quantity": 1
            }
        ],
        "text": "ТЕСТ!"
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == expected_status


@pytest.mark.django_db
def test_create_empty_collection(api_client, get_token):
    token = get_token(is_staff=True)
    url = reverse('product-collections-list')

    payload = {
        "title": "Тест",
        "positions": [],
        "text": "ТЕСТ!"
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_repeat_positions_order(api_client, get_token, product_factory):
    token = get_token(is_staff=True)
    product = product_factory()
    url = reverse('product-collections-list')

    payload = {
        "title": "Тест",
        "positions": [
            {
                "product_id": product.id,
                "quantity": 1
            },
            {
                "product_id": product.id,
                "quantity": 1
            }
        ],
        "text": "ТЕСТ!"
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_patch_collection(api_client, collection_factory, get_token):
    token = get_token(is_staff=True)
    collection = collection_factory()
    url = reverse('product-collections-detail', args=(collection.id, ))
    text = "NEW_TEXT"

    payload = {
        "text": text
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.patch(url, payload, format='json')
    assert resp.status_code == HTTP_200_OK
    collection.refresh_from_db()
    assert collection.text == text


@pytest.mark.django_db
def test_no_admin_patch_collection(api_client, collection_factory, get_token):
    token = get_token()
    collection = collection_factory()
    url = reverse('product-collections-detail', args=(collection.id, ))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.patch(url)
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_destroy_collection(api_client, collection_factory, get_token):
    token = get_token(is_staff=True)
    collection = collection_factory()
    url = reverse('product-collections-detail', args=(collection.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
