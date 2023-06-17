from django.urls import path

from . import views


app_name = "comments"
urlpatterns = [
    path("", views.CommentListView.as_view(), name="list"),
    path("add/", views.CommentCreateView.as_view(), name="add"),
]
