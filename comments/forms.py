import base64

from django import forms
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import Author, Comment


FIELD_WIDGET_ATTRS = {"class": "form-control mb-1"}


class CommentModelForm(forms.ModelForm):
    """Model form for the Comment model for creating a comment."""

    username = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        validators=[UnicodeUsernameValidator()],
        widget=forms.TextInput(attrs=FIELD_WIDGET_ATTRS),
        help_text="This value may contain only letters, numbers, and @/./+/-/_ characters.",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs=FIELD_WIDGET_ATTRS),
    )
    captcha = CaptchaField(widget=CaptchaTextInput(attrs=FIELD_WIDGET_ATTRS))

    def save(
        self,
        comment_parent_id: str | None,
        canvas_url: str | None,
        commit=False,
    ) -> None:
        """Creates a comment for new or exist author."""
        comment: Comment = super().save(commit)

        if comment_parent_id and comment_parent_id.isdigit():
            comment.parent = get_object_or_404(
                Comment, id=int(comment_parent_id)
            )
        comment.author = self._get_author()

        if canvas_url:
            comment.file.save(
                comment.file.name,
                self._get_image_file_from_(canvas_url, comment.file.name),
            )
        comment.save()

    def _get_author(self) -> Author:
        """Returns new or exist author."""
        author, _ = Author.objects.get_or_create(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
        )
        return author

    def _get_image_file_from_(
        self, canvas_url: str, filename: str
    ) -> ContentFile:
        """Returns content file from decoded canvas_url."""
        image_data = canvas_url.split(",")[1]
        return ContentFile(base64.b64decode(image_data), name=filename)

    class Meta:
        """Meta options for the CommentModelForm."""

        model = Comment
        fields = ("username", "email", "home_page", "captcha", "text", "file")
        labels = {
            "home_page": "Home page (optional)",
            "file": "Attached comment file (optional)",
        }
        widgets = {
            "home_page": forms.URLInput(attrs=FIELD_WIDGET_ATTRS),
            "text": forms.Textarea(attrs=FIELD_WIDGET_ATTRS),
            "file": forms.FileInput(
                attrs={
                    "class": "form-control mb-1",
                    "accept": ".jpg, .jpeg, .gif, .png, .txt",
                }
            ),
        }
