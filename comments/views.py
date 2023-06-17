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

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse | NoReturn:
        """Raises "Not found" if ordering is wrong else calls super method."""
        if self.get_ordering() is None:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Adds the CommentModelForm to context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["form"] = CommentModelForm()
        return context

    def get_ordering(self) -> str | None:
        """Returns ordering string or None after checking GET parameters."""
        order_by: str = self.request.GET.get("orderby") or "c"
        order_dir: str = self.request.GET.get("orderdir") or "desc"

        if services.are_ordering_parameters_valid(order_by, order_dir):
            return services.get_order_symbol_by_(
                order_dir
            ) + services.get_correct_(order_by)
        return None
