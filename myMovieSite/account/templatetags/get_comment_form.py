from django import template
from django.template.defaulttags import register
from ..models import comments
from django.contrib.contenttypes.models import ContentType
from ..forms import Commentforms
"""

@register.simple_tag
def get_comment_form(curr_movie,movie_id):
    content_type =curr_movie
    object_id = movie_id
    form = Commentforms(initial={
        'content_type': content_type,
        'object_id': object_id})
    return form
    """
