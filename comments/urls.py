from django.urls import path

from . import views


urlpatterns = [
    path("", views.CommentListView.as_view(), name="list"),
    path("add/", views.CommentCreateView.as_view(), name="add"),
]
