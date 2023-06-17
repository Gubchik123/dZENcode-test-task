from typing import Any, NoReturn
from django.views import generic
from django.http import HttpRequest, HttpResponse, Http404

from . import services
from .models import Comment
from .forms import CommentModelForm
from general.views import BaseView


class CommentListView(BaseView, generic.ListView):
    """View for displaying all comments."""

    model = Comment
    paginate_by = 25
    extra_context = {"form": CommentModelForm()}

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse | NoReturn:
        """Raises "Not found" if ordering is wrong else calls super method."""
        if self.get_ordering() is None:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_ordering(self) -> str | None:
        """Returns ordering string or None by the GET parameters."""
        return services.get_ordering_string(
            self.request.GET.get("orderby") or "c",
            self.request.GET.get("orderdir") or "desc",
        )
