from django.contrib import admin
from django.urls import path

from general.error_views import (
    CustomBadRequestView,
    CustomNotFoundView,
)


handler400 = CustomBadRequestView.as_view()
handler404 = CustomNotFoundView.as_view()

urlpatterns = [
    path("admin/", admin.site.urls),
]
