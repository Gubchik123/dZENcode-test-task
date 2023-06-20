from typing import NoReturn

from django.urls import path
from django.views import View
from django.test import TestCase
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, Http404

from general.error_views import (
    ErrorView,
    CustomBadRequestView,
    CustomNotFoundView,
    CustomServerErrorView,
)
from general.views import BaseView
from spa.urls import urlpatterns, handler400, handler404


class RaiseExceptionView(View):
    """View that raises the exception attribute."""

    exception: Exception

    def get(self, request: HttpRequest) -> NoReturn:
        """Raises the specified exception."""
        raise self.exception


class RaiseBadRequestView(RaiseExceptionView):
    """View that raises a 400 Bad Request exception."""

    exception = BadRequest


class RaiseNotFoundView(RaiseExceptionView):
    """View that raises a 404 Not Found exception."""

    exception = Http404


class ServerErrorView(BaseView, View):
    """View that has error."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Has error before returns response."""
        print(1 / 0)  # ZeroDivisionError
        return HttpResponse("Some content")


# Adding URLs for testing custom error handlers.
# Because the custom error page extends _base.html,
# where there are some links by view names such as "faq" and "about".
urlpatterns += [
    path("400/", RaiseBadRequestView.as_view()),
    path("404/", RaiseNotFoundView.as_view()),
    path("500/", ServerErrorView.as_view()),
]


class CustomErrorHandlerTestMixin:
    """Test mixin for custom error handlers."""

    error_handler: ErrorView

    def setUp(self):
        """Gets response with test client by generated url attribute."""
        self.response = self.client.get(f"/{self.error_handler.code}/")

    def test_view_status_code(self):
        """Tests response status code matches code attribute."""
        self.assertEqual(self.response.status_code, self.error_handler.code)

    def test_view_template(self):
        """Tests response template matches template_name attribute."""
        self.assertTemplateUsed(self.response, "error.html")

    def test_view_content(self):
        """Tests response content."""
        self.assertContains(
            self.response,
            self.error_handler.name,
            status_code=self.error_handler.code,
        )
        self.assertContains(
            self.response,
            self.error_handler.description,
            status_code=self.error_handler.code,
        )


class CustomBadRequestViewTest(CustomErrorHandlerTestMixin, TestCase):
    """Tests for CustomBadRequestView."""

    error_handler = CustomBadRequestView


class CustomNotFoundViewTest(CustomErrorHandlerTestMixin, TestCase):
    """Tests for CustomNotFoundView."""

    error_handler = CustomNotFoundView


class CustomServerErrorViewTest(CustomErrorHandlerTestMixin, TestCase):
    """Tests for CustomServerErrorView."""

    error_handler = CustomServerErrorView
