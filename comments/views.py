from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentPagination(PageNumberPagination):
    page_size = 25


class CommentListCreateView(generics.ListCreateAPIView):

    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):

        queryset = (
            Comment.objects
            .filter(parent=None)
            .prefetch_related("replies")
        )

        sort = self.request.GET.get("sort")

        allowed_sorts = {
            "username": "username",
            "-username": "-username",
            "email": "email",
            "-email": "-email",
            "date": "created_at",
            "-date": "-created_at",
        }

        queryset = queryset.order_by(allowed_sorts.get(sort, "-created_at"))

        return queryset
