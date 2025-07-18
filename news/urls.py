from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("article/<str:article_title>/<int:article_id>", views.article, name="article"),
    path("news/", views.NewsListView.as_view(), name="news"),
    path("columns/", views.ColumnsListView.as_view(), name="columns"),
    path("interviews/", views.InterviewsListView.as_view(), name="interviews"),
    path("search/", views.search, name="search"),
    path("author/<str:author_name>/<int:author_id>", views.author, name="author")
]