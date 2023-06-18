import base64

from django import forms
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
            comment.parent_id = int(comment_parent_id)

        author, _ = Author.objects.get_or_create(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
        )
        comment.author = author

        if canvas_url:
            image_data = canvas_url.split(",")[1]
            image_file = ContentFile(
                base64.b64decode(image_data), name=comment.file.name
            )
            comment.file.save(comment.file.name, image_file)

        comment.save()

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
