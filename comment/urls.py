from django.urls import path

from .views import CommentPostView
urlpatterns=[
    path("post_comment/<int:article_id>",CommentPostView.as_view(),name="post_comment"),
    path("post_comment/<int:article_id>/<int:parent_comment_id>",CommentPostView.as_view(),name="comment_reply"),
]