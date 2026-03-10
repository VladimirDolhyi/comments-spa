from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from comments.models import Comment
from comments.serializers import CommentSerializer, PreviewSerializer
from comments.validators import clean_comment_text, validate_xhtml


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
