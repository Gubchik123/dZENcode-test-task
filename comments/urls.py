from django.urls import path

from . import views


app_name = "comment"
urlpatterns = [path("", views.CommentListView.as_view(), name="list")]
