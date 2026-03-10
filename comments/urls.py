from django.urls import path
from comments.views import CommentListCreateView
from comments.views import CaptchaAPIView

urlpatterns = [
    path("comments/", CommentListCreateView.as_view(), name="comment-list"),
    path("captcha/", CaptchaAPIView.as_view() , name="captcha"),
]
app_name = "comments"
