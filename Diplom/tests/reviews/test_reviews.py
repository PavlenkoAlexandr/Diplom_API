import random
import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
     HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_list_reviews(api_client, reviews_factory, get_token):
    token = get_token(is_staff=False)
    url = reverse('product-reviews-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_list_reviews(api_client, reviews_factory):
    review = reviews_factory()
    url = reverse('product-reviews-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert review.id


@pytest.mark.django_db
def test_get_review(api_client, reviews_factory, get_token):
    token = get_token()
    review = reviews_factory()
    url = reverse('product-reviews-detail', args=(review.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert resp.json()['id'] == review.id


@pytest.mark.django_db
def test_unauthorized_get_review(api_client, reviews_factory):
    review = reviews_factory()
    url = reverse('product-reviews-detail', args=(review.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert review.id


@pytest.mark.parametrize(
    ["rating", "expected_status"],
    (
            (1, HTTP_201_CREATED),
            (0, HTTP_400_BAD_REQUEST),
            (6, HTTP_400_BAD_REQUEST)
    )
)
@pytest.mark.django_db
def test_create_review(api_client, get_token, product_factory, rating, expected_status):
    token = get_token()
    product = product_factory()
    url = reverse('product-reviews-list')

    payload = {
            "product_id": product.id,
            "text": "ТЕСТ!",
            "rating": rating
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == expected_status


@pytest.mark.django_db
def test_create_second_review(api_client, product_factory, reviews_factory, user_for_test):
    product = product_factory()
    review = reviews_factory(product_id=product, author_id=user_for_test['user'])
    url = reverse('product-reviews-list')

    payload = {
            "product_id": product.id,
            "text": "ТЕСТ!",
            "rating": 1
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_for_test['token'])
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_unauthorized_create_review(api_client, product_factory):
    product = product_factory()
    url = reverse('product-reviews-list')

    payload = {
        "product_id": product.id,
        "text": "ТЕСТ!",
        "rating": 1
    }

    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_patch_review(api_client, reviews_factory, get_token, user_for_test):
    review = reviews_factory(author_id=user_for_test['user'])
    url = reverse('product-reviews-detail', args=(review.id,))
    rating = random.randint(1, 5)

    payload = {
        "rating": rating
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_for_test['token'])
    resp = api_client.patch(url, payload, format='json')
    assert resp.status_code == HTTP_200_OK
    review.refresh_from_db()
    assert review.rating == rating


@pytest.mark.django_db
def test_destroy_review(api_client, reviews_factory, get_token):
    review = reviews_factory()
    token = get_token(is_staff=True)
    url = reverse('product-reviews-detail', args=(review.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
