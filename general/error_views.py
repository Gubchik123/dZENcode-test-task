from typing import NamedTuple

from django.views import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template.exceptions import TemplateDoesNotExist


class Error(NamedTuple):
    """Named tuple that holds information about an error."""

    code: int
    name: str
    description: str


def render_error_page(request: HttpRequest, error: Error) -> HttpResponse:
    """Renders error page (if template exist) by given error."""
    try:
        return render(
            request, "error.html", {"error": error}, status=error.code
        )
    except TemplateDoesNotExist:
        return HttpResponse(
            f"""
            <title>{error.code} | LapZone</title>
            <h1>{error.name}</h1>
            <h4>{error.description}</h4>
            """,
            status=error.code,
        )


class ErrorView(View):
    """Base error view for rendering the custom error page."""

    code: int
    name: str
    description: str

    def get(self, request: HttpRequest, exception=None) -> HttpResponse:
        """Returns the custom error page with the given error information."""
        return render_error_page(
            request, Error(self.code, self.name, self.description)
        )


class CustomBadRequestView(ErrorView):
    """Custom view for handling the 400 HTTP status code."""

    code = 400
    name = "Bad Request"
    description = "The server cannot or will not process the request."


class CustomNotFoundView(ErrorView):
    """Custom view for handling the 404 HTTP status code."""

    code = 404
    name = "Not Found"
    description = (
        "The server cannot find the requested resource. URL is not recognized."
    )


class CustomServerErrorView(ErrorView):
    """Custom view for handling the 500 HTTP status code."""

    code = 500
    name = "Internal Server Error"
    description = "Sorry, an error occurred in the server. Try again."
