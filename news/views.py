from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from .models import *

def index(request):
    news = Article.objects.filter(article_type="news").order_by("-date")[:3]
    columns = Article.objects.filter(article_type="column").order_by("-date")[:2]
    interviews = Article.objects.filter(article_type="interview").order_by("-date")[:3]

    context = {
        "news": news,
        "columns": columns,
        "interviews": interviews
    }
    return render(request, "news/index.html", context)


@cache_page(60 * 15)
def article(request, article_title, article_id):
    article = get_object_or_404(Article, pk=article_id)
    recommendations = Article.objects.filter(tags__in=article.tags.all()).distinct().exclude(id=article_id).order_by("-date")[:3]

    context = {
        "article": article,
        "recommendations": recommendations
    }

    return redirect("article", slugify(article.title, allow_unicode=True), article_id) \
        if slugify(article.title, allow_unicode=True) != article_title else render(request, "news/article.html", context)


class NewsListView(ListView):
    paginate_by = 12
    model = Article
    ordering = ["-date"]
    template_name = "news/news.html"
    queryset = Article.objects.filter(article_type="news")


class ColumnsListView(ListView):
    paginate_by = 14
    model = Article
    ordering = ["-date"]
    template_name = "news/columns.html"
    queryset = Article.objects.filter(article_type="column")


class InterviewsListView(ListView):
    paginate_by = 8
    model = Article
    ordering = ["-date"]
    template_name = "news/interviews.html"
    queryset = Article.objects.filter(article_type="interview")