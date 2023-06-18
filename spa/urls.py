from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from general.error_views import (
    CustomBadRequestView,
    CustomNotFoundView,
)


handler400 = CustomBadRequestView.as_view()
handler404 = CustomNotFoundView.as_view()

urlpatterns = [
    path("captcha/", include("captcha.urls")),
    path("", include("comments.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
