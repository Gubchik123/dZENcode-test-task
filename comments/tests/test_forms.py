from django import forms
from django.test import SimpleTestCase
from captcha.fields import CaptchaTextInput
from django.contrib.auth.validators import UnicodeUsernameValidator

from comments.models import Comment
from comments.forms import CommentModelForm, FIELD_WIDGET_ATTRS


FIELD_WIDGET_CLASS = FIELD_WIDGET_ATTRS["class"]


class CommentModelFormSimpleTestCase(SimpleTestCase):
    """Tests for the CommentModelForm."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the CommentModelForm for testing."""
        super().setUpClass()
        cls.form = CommentModelForm()

    # * ---------- Testing the meta options of the CommentModelForm -----------

    def test_form_model(self):
        """Tests the form model."""
        self.assertEqual(self.form._meta.model, Comment)

    def test_form_fields(self):
        """Tests the form fields."""
        self.assertEqual(
            tuple(self.form._meta.fields),
            ("username", "email", "home_page", "captcha", "text", "file"),
        )

    def test_home_page_label(self):
        """Tests the home page label."""
        self.assertEqual(
            self.form.fields["home_page"].label, "Home page (optional)"
        )

    def test_file_label(self):
        """Tests the file label."""
        self.assertEqual(
            self.form.fields["file"].label, "Attached comment file (optional)"
        )

    def test_home_page_widget(self):
        """Tests the home page widget."""
        self.assertIsInstance(
            self.form.fields["home_page"].widget, forms.URLInput
        )

    def test_home_page_widget_attrs_class(self):
        """Tests the home page widget attrs class."""
        self.assertEqual(
            self.form.fields["home_page"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    def test_text_widget(self):
        """Tests the text widget."""
        self.assertIsInstance(self.form.fields["text"].widget, forms.Textarea)

    def test_text_widget_attrs_class(self):
        """Tests the home page widget attrs class."""
        self.assertEqual(
            self.form.fields["home_page"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    def test_file_widget(self):
        """Tests the file widget."""
        self.assertIsInstance(self.form.fields["file"].widget, forms.FileInput)

    def test_file_widget_attrs_class(self):
        """Tests the file widget attrs class."""
        self.assertEqual(
            self.form.fields["file"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    def test_file_widget_attrs_accept(self):
        """Tests the file widget attrs accept."""
        self.assertEqual(
            self.form.fields["file"].widget.attrs["accept"],
            ".jpg, .jpeg, .gif, .png, .txt",
        )

    # * ---------------- Test the 'username' field parameters -----------------

    def test_username_max_length(self):
        """Tests the username max length."""
        self.assertEqual(self.form.fields["username"].max_length, 100)

    def test_username_min_length(self):
        """Tests the username min length."""
        self.assertEqual(self.form.fields["username"].min_length, 2)

    def test_username_required(self):
        """Tests the username required."""
        self.assertTrue(self.form.fields["username"].required)

    def test_username_validator(self):
        """Tests the username validator."""
        self.assertIsInstance(
            self.form.fields["username"].validators[0],
            UnicodeUsernameValidator,
        )

    def test_username_widget(self):
        """Tests the username widget."""
        self.assertIsInstance(
            self.form.fields["username"].widget, forms.TextInput
        )

    def test_username_widget_attrs_class(self):
        """Tests the username widget attrs class."""
        self.assertEqual(
            self.form.fields["username"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    # * ---------------- Test the 'email' field parameters --------------------

    def test_email_required(self):
        """Tests the email required."""
        self.assertTrue(self.form.fields["email"].required)

    def test_email_widget(self):
        """Tests the email widget."""
        self.assertIsInstance(
            self.form.fields["email"].widget,
            forms.EmailInput,
        )

    def test_email_widget_attrs_class(self):
        """Tests the email widget attrs class."""
        self.assertEqual(
            self.form.fields["email"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    # * ---------------- Test the 'captcha' field parameters ------------------

    def test_captcha_widget(self):
        """Tests the captcha widget."""
        self.assertIsInstance(
            self.form.fields["captcha"].widget, CaptchaTextInput
        )
