import logging

from django import http
from django.core.exceptions import BadRequest

from .error_views import Error, CustomServerErrorView, render_error_page

logger = logging.getLogger(__name__)


class BaseView:
    """Base view for all other views with exception handling."""

    def dispatch(
        self, request: http.HttpRequest, *args, **kwargs
    ) -> http.HttpResponse:
        """Handles exceptions during dispatch and returns a response."""
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            exception_type = type(e)

            # Check if it's an exception for which there is an error handler.
            if exception_type in (http.Http404, BadRequest):
                raise e

            logger.error(
                f"{exception_type}('{str(e)}') during working with {request.path} URL"
            )

            error_view = CustomServerErrorView
            return render_error_page(
                request,
                Error(
                    error_view.code, error_view.name, error_view.description
                ),
            )
