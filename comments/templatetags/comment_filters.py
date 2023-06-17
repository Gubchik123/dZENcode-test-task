from django import template
from django.template.loader import render_to_string

from comments.models import Comment


register = template.Library()


@register.filter
def render_comments(comment: Comment) -> str:
    html = ""
    if comment:
        html += render_to_string(
            "comments/utils/_comment.html", {"comment": comment}
        )
        for child_comment in comment.comment_set.all():
            html += f"<div class='child-comments'>{render_comments(child_comment)}</div>"
        html += "</div>"
    return html
