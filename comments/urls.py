from django.urls import path
from comments.views import CommentListCreateView
from comments.views import CaptchaAPIView
from comments.views import CommentPreviewAPIView

urlpatterns = [
    path("comments/", CommentListCreateView.as_view(), name="comment-list"),
    path("captcha/", CaptchaAPIView.as_view() , name="captcha"),
    path("preview/", CommentPreviewAPIView.as_view(), name="preview"),
]
app_name = "comments"
