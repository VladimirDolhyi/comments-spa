from django.urls import path
from comments.views import CommentListCreateView

urlpatterns = [
    path("comments/", CommentListCreateView.as_view()),
]
app_name = "comments"
