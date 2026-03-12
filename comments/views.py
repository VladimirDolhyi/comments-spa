from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.views.generic import TemplateView
from django.db.models import Prefetch

from comments.models import Comment
from comments.serializers import CommentSerializer, PreviewSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class CommentPagination(PageNumberPagination):
    page_size = 25


class CommentListCreateView(generics.ListCreateAPIView):

    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):

        replies = Comment.objects.all().order_by("created_at")

        queryset = (
            Comment.objects
            .filter(parent=None)
            .prefetch_related(
                Prefetch("replies", queryset=replies)))

        sort = self.request.GET.get("sort")

        allowed_sorts = {
            "username": "username",
            "-username": "-username",
            "email": "email",
            "-email": "-email",
            "date": "created_at",
            "-date": "-created_at",
        }

        return queryset.order_by(allowed_sorts.get(sort, "-created_at"))

    def perform_create(self, serializer):
        comment = serializer.save()

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "comments",
            {
                "type": "new_comment",
                "data": {
                    "user": comment.username,
                    "text": comment.text,
                    "created": str(comment.created_at)
                }
            }
        )


class CaptchaAPIView(APIView):

    def get(self, request):
        key = CaptchaStore.generate_key()

        return Response({
            "captcha_key": key,
            "captcha_image": captcha_image_url(key)
        })


class CommentPreviewAPIView(generics.GenericAPIView):

    serializer_class = PreviewSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "preview": serializer.validated_data["text"]
        })


class IndexView(TemplateView):
    template_name = "index.html"
