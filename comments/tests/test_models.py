from django.test import TestCase
from django.db.models import Model

from comments.models import Author, Comment


class _ModelMetaOptionsTestMixin:
    """Mixin for testing the base meta options of models."""

    model: Model
    verbose_name: str
    verbose_name_plural: str
    ordering: list[str]

    def test_model_verbose_name(self):
        """
        Test that the model's verbose name is equal to the verbose_name attribute.
        """
        self.assertEqual(self.model._meta.verbose_name, self.verbose_name)

    def test_model_verbose_name_plural(self):
        """
        Test that the model's verbose name (plural) is equal to the verbose_name_plural attribute.
        """
        self.assertEqual(
            self.model._meta.verbose_name_plural, self.verbose_name_plural
        )

    def test_model_fields_ordering(self):
        """
        Test that the model's ordering is equal to the ordering attribute.
        """
        self.assertEqual(self.model._meta.ordering, self.ordering)


class AuthorModelTestCase(_ModelMetaOptionsTestMixin, TestCase):
    """Tests for the Author model."""

    model = Author
    ordering = ["username"]
    verbose_name = "Comment author"
    verbose_name_plural = "Comment authors"

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first Author for testing."""
        Author.objects.create(username="test_user", email="test@gmail.com")

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        obj = self.model.objects.first()
        self.assertEqual(str(obj), obj.username)

    # * ---------------- Test the 'username' field parameters -----------------

    def test_username_max_length(self):
        """Tests that the username field has max_length=100."""
        self.assertEqual(
            self.model._meta.get_field("username").max_length, 100
        )

    def test_username_unique(self):
        """Tests that the username field is unique=False."""
        self.assertFalse(self.model._meta.get_field("username").unique)

    def test_username_blank(self):
        """Tests that the username field is blank=False."""
        self.assertFalse(self.model._meta.get_field("username").blank)

    def test_username_null(self):
        """Tests that the username field is null=False."""
        self.assertFalse(self.model._meta.get_field("username").null)

    def test_username_verbose_name(self):
        """Tests that the username field has verbose_name='Username'."""
        self.assertEqual(
            self.model._meta.get_field("username").verbose_name, "Username"
        )

    # * ----------------- Test the 'email' field parameters -------------------

    def test_email_unique(self):
        """Tests that the email field is unique=False."""
        self.assertFalse(self.model._meta.get_field("email").unique)

    def test_email_blank(self):
        """Tests that the email field is blank=False."""
        self.assertFalse(self.model._meta.get_field("email").blank)

    def test_email_null(self):
        """Tests that the email field is null=False."""
        self.assertFalse(self.model._meta.get_field("email").null)

    def test_email_verbose_name(self):
        """Tests that the email field has verbose_name='Email address'."""
        self.assertEqual(
            self.model._meta.get_field("email").verbose_name, "Email address"
        )


class CommentModelTestCase(_ModelMetaOptionsTestMixin, TestCase):
    """Tests for the Comment model."""

    model = Comment
    ordering = ["-created"]
    verbose_name = "Comment"
    verbose_name_plural = "Comments"

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first Comment for testing."""
        cls.author = Author.objects.create(
            username="test_user", email="test@gmail.com"
        )
        Comment.objects.create(
            text="test comment", author=cls.author, parent=None
        )

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        obj = self.model.objects.first()
        self.assertEqual(str(obj), f"{obj.pk} from {obj.author}")

    # * ---------------- Test the 'home_page' field parameters ----------------

    def test_home_page_blank(self):
        """Tests that the home_page field is blank=True."""
        self.assertTrue(self.model._meta.get_field("home_page").blank)

    def test_home_page_null(self):
        """Tests that the home_page field is null=True."""
        self.assertTrue(self.model._meta.get_field("home_page").null)

    def test_home_page_verbose_name(self):
        """Tests that the home_page field has verbose_name='Home page'."""
        self.assertEqual(
            self.model._meta.get_field("home_page").verbose_name, "Home page"
        )

    # * ---------------- Test the 'text' field parameters ---------------------

    def test_text_blank(self):
        """Tests that the text field is blank=False."""
        self.assertFalse(self.model._meta.get_field("text").blank)

    def test_text_null(self):
        """Tests that the text field is null=False."""
        self.assertFalse(self.model._meta.get_field("text").null)

    def test_text_verbose_name(self):
        """Tests that the text field has verbose_name='Comment body'."""
        self.assertEqual(
            self.model._meta.get_field("text").verbose_name, "Comment body"
        )

    # * ----------------- Test the 'file' field parameters --------------------

    def test_file_upload_to(self):
        """Tests that the file field has upload_to='comment_files/'."""
        self.assertEqual(
            self.model._meta.get_field("file").upload_to, "comment_files/"
        )

    def test_file_blank(self):
        """Tests that the file field is blank=True."""
        self.assertTrue(self.model._meta.get_field("file").blank)

    def test_file_null(self):
        """Tests that the file field is null=True."""
        self.assertTrue(self.model._meta.get_field("file").null)

    def test_file_verbose_name(self):
        """Tests that the file field has verbose_name='Attached comment file'."""
        self.assertEqual(
            self.model._meta.get_field("file").verbose_name,
            "Attached comment file",
        )

    # * ---------------- Test the 'created' field parameters ------------------

    def test_created_auto_now_add(self):
        """Tests that the created field has auto_now_add=True."""
        self.assertTrue(self.model._meta.get_field("created").auto_now_add)

    def test_created_verbose_name(self):
        """Tests that the created field has verbose_name='Created datetime'."""
        self.assertEqual(
            self.model._meta.get_field("created").verbose_name,
            "Created datetime",
        )

    # * ---------------- Test the 'parent' field parameters -------------------

    def test_parent_null(self):
        """Tests that the parent field is null=True."""
        self.assertTrue(self.model._meta.get_field("parent").null)

    def test_parent_blank(self):
        """Tests that the parent field is blank=True."""
        self.assertTrue(self.model._meta.get_field("parent").blank)

    def test_parent_default(self):
        """Tests that the parent field has default=None."""
        self.assertIsNone(self.model._meta.get_field("parent").default)

    def test_parent_verbose_name(self):
        """Tests that the parent field has verbose_name='Parent comment'."""
        self.assertEqual(
            self.model._meta.get_field("parent").verbose_name, "Parent comment"
        )

    def test_parent_on_delete(self):
        """Tests that the parent field on_delete is CASCADE."""
        Comment.objects.get(id=1).delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=1)

    # * ---------------- Test the 'author' field parameters -------------------

    def test_author_verbose_name(self):
        """Tests that the author field has verbose_name='Comment author'."""
        self.assertEqual(
            self.model._meta.get_field("author").verbose_name, "Comment author"
        )

    def test_author_on_delete(self):
        """Tests that the author field on_delete is CASCADE."""
        Comment.objects.get(id=1).delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=1)
