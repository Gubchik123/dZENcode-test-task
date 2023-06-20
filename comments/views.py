from typing import Any, Dict, NoReturn

from django import http
from django.views import generic
from django.contrib import messages

from . import services
from .models import Comment
from .forms import CommentModelForm
from general.views import BaseView


FORM_DATA = {}


class CommentListView(BaseView, generic.ListView):
    """View for displaying all comments."""

    paginate_by = 25
    queryset = Comment.objects.all().filter(parent_id__isnull=True)

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse | NoReturn:
        """Raises "Not found" if ordering is wrong else calls super method."""
        if self.get_ordering() is None:
            raise http.Http404
        return super().get(request, *args, **kwargs)

    def get_ordering(self) -> str | None:
        """Returns ordering string or None by the GET parameters."""
        return services.get_ordering_string(
            self.request.GET.get("orderby") or "c",
            self.request.GET.get("orderdir") or "desc",
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Adds the form to the context and returns it."""
        global FORM_DATA
        context = super().get_context_data(**kwargs)
        context["form"] = CommentModelForm(FORM_DATA or None)
        FORM_DATA = {}
        return context


class CommentCreateView(BaseView, generic.CreateView):
    """View for handling only POST request and creating a comment."""

    model = Comment
    success_url = "/"
    http_method_names = ["post"]
    form_class = CommentModelForm

    def form_valid(self, form: CommentModelForm) -> http.HttpResponseRedirect:
        """Saves the form,
        adds the success message and returns redirect to the success_url."""
        comment_parent_id = self.request.POST.get("comment_parent_id", None)
        canvas_url = self.request.POST.get("resized_image", None)
        form.save(comment_parent_id, canvas_url)

        s = "comment" if not comment_parent_id else "answer"
        messages.success(self.request, f"Your {s} has successfully added.")
        return http.HttpResponseRedirect(self.success_url)

    def form_invalid(
        self, form: CommentModelForm
    ) -> http.HttpResponseRedirect:
        """Adds error message and returns redirect to the success_url."""
        global FORM_DATA
        FORM_DATA = self.request.POST
        
        messages.error(self.request, "Invalid form data.")
        return http.HttpResponseRedirect(self.success_url)
