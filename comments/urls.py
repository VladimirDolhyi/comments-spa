from django.urls import path
from comments.views import CommentListCreateView

urlpatterns = [
    path("", CommentListCreateView.as_view(), name="comment-list"),
]
app_name = "comments"
