from django.db import models


class Author(models.Model):
    """A model representing a comment author."""

    username = models.CharField(
        max_length=100,
        unique=False,
        blank=False,
        null=False,
        verbose_name="Username",
    )
    email = models.EmailField(
        unique=False, blank=False, null=False, verbose_name="Email address"
    )

    def __str__(self) -> str:
        """Returns string representation of the Author model."""
        return self.username

    class Meta:
        """Meta options for the Author model."""

        ordering = ["username"]
        verbose_name = "Comment author"
        verbose_name_plural = "Comment authors"


class _CommentCustomManager(models.Manager):
    """Custom manager for the Comment model."""

    def all(self):
        """Returns all comments using the select_related for the 'parent'."""
        return super().all().select_related("parent")


class Comment(models.Model):
    """A model representing a comment."""

    home_page = models.URLField(
        blank=True, null=True, verbose_name="Home page"
    )
    text = models.TextField(
        blank=False, null=False, verbose_name="Comment body"
    )
    file = models.FileField(
        upload_to="comment_files/",
        blank=True,
        null=True,
        verbose_name="Attached comment file",
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created datetime"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="Parent comment",
    )

    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name="Comment author"
    )

    objects = _CommentCustomManager()

    def __str__(self) -> str:
        """Returns string representation of the Comment model."""
        return f"{self.pk} from {self.author}"

    class Meta:
        """Meta options for the Comment model."""

        ordering = ["-created"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
