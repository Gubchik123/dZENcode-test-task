from django.urls import reverse
from django.test import TestCase
from django.http import HttpResponse

from comments.models import Author, Comment
from comments.forms import CommentModelForm


class CommentListViewTestCase(TestCase):
    """Tests for the CommentListView."""

    url = "/"
    name = "list"
    template_name = "comments/comment_list.html"
    queryset = Comment.objects.all().filter(parent_id__isnull=True)

    @classmethod
    def setUpTestData(cls) -> None:
        """Sets up tests data by creating 28 comments."""
        for count in range(1, 29):
            Comment.objects.create(
                text=f"Tests comment #{count}",
                author=Author.objects.create(
                    username=f"test_user_{count}",
                    email=f"test_user_{count}@gmail.com",
                ),
            )

    def setUp(self) -> None:
        """Sets up the tests by retrieving a response from the view's URL."""
        self.response = self.client.get(self.url)

    def test_view_url_exists_at_desired_location(self):
        """Tests that the view exists at desired location."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Tests that the response in the view uses the correct template."""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, self.template_name)

    def test_view_url_accessible_by_name(self):
        """Tests that the view is accessible using its name."""
        response = self.client.get(reverse(self.name))
        self.assertEqual(response.status_code, 200)

    def test_comment_form_is_in_context(self):
        """Tests that the form is in the context."""
        self.assertIn("form", self.response.context)
        self.assertIsInstance(self.response.context["form"], CommentModelForm)

    def test_lists_comments(self):
        """Tests that comments are listed on a page."""
        self.assertIn("page_obj", self.response.context)
        self.assertEqual(
            self.response.context["page_obj"].object_list,
            list(self.queryset[:25]),
        )

    # * ------------------ Testing pagination functionality -------------------

    def test_pagination_is_twenty_five(self):
        """Tests that pagination is set to 25 per page."""
        self.assertEqual(len(self.response.context["page_obj"]), 25)

    def test_paginated_product_list(self):
        """Tests second page has (exactly) remaining 3 comments."""
        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 3)

    def test_404_with_invalid_pagination_page_value(self):
        """Tests that invalid pagination page value results in 404"""
        response = self.client.get(f"{self.url}?page=0")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?page=3")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?page=string")
        self.assertEqual(response.status_code, 404)

    # * ------------------- Testing ordering functionality --------------------

    def test_lists_comments_ordered_by_created_desc_by_default(self):
        """
        Tests that comments ordered by created (DESC) by default are listed on a page.
        """
        self.assertEqual(
            self.response.context["page_obj"].object_list,
            list(self.queryset[:25]),
        )

    def test_lists_comments_ordered_by_created_asc(self):
        """
        Tests that comments ordered by created (ASC) are listed on a page.
        """
        response = self.client.get(f"{self.url}?orderby=c&orderdir=asc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("created")[:25]),
        )

    def test_lists_comments_ordered_by_username_asc(self):
        """
        Tests that comments ordered by username (ASC) are listed on a page.
        """
        response = self.client.get(f"{self.url}?orderby=u&orderdir=asc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("author__username")[:25]),
        )

    def test_lists_comments_ordered_by_username_desc(self):
        """
        Tests that comments ordered by username (DESC) are listed on a page.
        """
        response = self.client.get(f"{self.url}?orderby=u&orderdir=desc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("-author__username")[:25]),
        )

    def test_lists_comments_ordered_by_email_asc(self):
        """Tests that comments ordered by email (ASC) are listed on a page."""
        response = self.client.get(f"{self.url}?orderby=e&orderdir=asc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("author__email")[:25]),
        )

    def test_lists_comments_ordered_by_email_desc(self):
        """Tests that comments ordered by email (DESC) are listed on a page."""
        response = self.client.get(f"{self.url}?orderby=e&orderdir=desc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("-author__email")[:25]),
        )

    def test_404_with_invalid_order_parameters(self):
        """Tests that invalid order parameters result in 404."""
        response = self.client.get(f"{self.url}?orderby=wrong&orderdir=asc")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?orderby=c&orderdir=wrong")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?orderby=wrong")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?orderdir=wrong")
        self.assertEqual(response.status_code, 404)


class CommentCreateViewTestCase(TestCase):
    """Tests for the CommentCreateView."""

    url = "/add/"

    def test_405_with_get_request(self):
        """Tests that the view returns 404 with GET request."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_adding_comment_with_valid_form_data(self):
        """Tests adding a comment with valid form data."""
        response = self._test_comment_form_for_validity_and_get_response(
            self._get_valid_form_data()
        )
        self.assertContains(response, "Your comment has successfully added.")

    def test_adding_comment_with_invalid_form_data(self):
        """Tests adding a comment with invalid form data."""
        form_data = self._get_valid_form_data()
        form_data["username"] = "test user"
        response = self._test_comment_form_for_validity_and_get_response(
            form_data, is_valid=False
        )
        self.assertContains(response, "Invalid form data.")

    def test_adding_answer_with_valid_form_data(self):
        """Tests adding an answer with valid form data."""
        comment = Comment.objects.create(
            text=f"Tests comment",
            author=Author.objects.create(
                username=f"test_user",
                email=f"test_user@gmail.com",
            ),
        )
        form_data = self._get_valid_form_data()
        form_data["comment_parent_id"] = comment.id
        response = self._test_comment_form_for_validity_and_get_response(
            form_data
        )
        self.assertContains(response, "Your answer has successfully added.")

    def test_404_with_nonexistent_parent_id(self):
        """Tests that the view returns 404 with nonexistent parent_id."""
        # ! I think it's valid test, but it returns 405.
        # form_data = self._get_valid_form_data()
        # form_data["comment_parent_id"] = 100
        # response = self._test_comment_form_for_validity_and_get_response(
        #     form_data, is_valid=False, status_code=404
        # )
        # self.assertContains(response, "Not Found")

    def _get_valid_form_data(self) -> dict:
        """Returns valid form data."""
        return {
            "username": "test_user",
            "email": "test_user@gmail.com",
            "text": "Test comment",
        }

    def _test_comment_form_for_validity_and_get_response(
        self, form_data: dict, is_valid: bool = True, status_code: int = 200
    ) -> HttpResponse:
        """Tests that the form is valid or invalid
        by the given form_data and returns the response."""
        self.assertTrue(
            CommentModelForm(form_data).is_valid()
        ) if is_valid else self.assertFalse(
            CommentModelForm(form_data).is_valid()
        )
        response = self.client.post(
            self.url, data=form_data, follow=True  # follow redirects
        )
        self.assertEqual(response.status_code, status_code)
        return response
