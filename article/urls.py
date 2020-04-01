from django.urls import path,re_path

from .views import ArticleView,ArticelDetail,ArticleCreate,ArticleDelete,ArticleUpdate

urlpatterns=[
    path('list',ArticleView.as_view(),name='list'),
    path('detail/<int:pk>/',ArticelDetail.as_view(),name="detail"),
    path('create/',ArticleCreate.as_view(),name="create"),
    path('delete/<int:pk>/',ArticleDelete.as_view(),name="delete"),
    path('update/<int:pk>/',ArticleUpdate.as_view(),name='update'),
]