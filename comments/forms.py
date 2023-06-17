from django import forms
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

    def save(self, commit=False) -> Comment:
        """Creates a comment for new or exist author."""
        comment: Comment = super().save(commit)
        author, _ = Author.objects.get_or_create(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
        )
        comment.author = author
        comment.save()
        return comment

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
            "file": forms.FileInput(attrs=FIELD_WIDGET_ATTRS),
        }
