from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from comments.models import Comment
from comments.serializers import CommentSerializer, PreviewSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.shortcuts import render


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

        return queryset.order_by(allowed_sorts.get(sort, "-created_at"))


class CaptchaAPIView(APIView):

    def get(self, request):
        key = CaptchaStore.generate_key()

        return Response({
            "captcha_key": key,
            "captcha_image": captcha_image_url(key)
        })


class CommentPreviewAPIView(APIView):

    def post(self, request):

        serializer = PreviewSerializer(data=request.data)

        if serializer.is_valid():
            return Response({
                "preview": serializer.validated_data["text"]
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


def create_comment(request):

    comment = Comment.objects.create(...)

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "comments",
        {
            "type": "new_comment",
            "data": {
                "user": comment.user_name,
                "text": comment.text,
                "created": str(comment.created_at)
            }
        }
    )


def index(request):
    return render(request, "index.html")
