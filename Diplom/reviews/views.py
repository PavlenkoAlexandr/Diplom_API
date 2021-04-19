from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from reviews.filters import ReviewsFilterSet
from reviews.models import Review
from reviews.permissions import IsAuthor
from reviews.serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewsFilterSet
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_permissions(self):
        if self.action in ['list', 'create', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthor()]

    def create(self, request, *args, **kwargs):
        request.data['author_id'] = request.user.id
        return super(ReviewViewSet, self).create(request)
