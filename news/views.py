from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView

from .models import *

def index(request):
    articles = Article.objects.all().values()

    # add slug from the title to the dict
    for item in articles:
        item["slug"] = slugify(item["title"], allow_unicode=True)

    context = {
        "articles": articles
    }
    return render(request, "news/index.html", context)

def article(request, article_title, article_id):
    article = get_object_or_404(Article, pk=article_id)

    context = {
        "article": article
    }

    return redirect("article", slugify(article.title, allow_unicode=True), article_id) \
        if slugify(article.title, allow_unicode=True) != article_title else render(request, "news/article.html", context)


class NewsListView(ListView):
    paginate_by = 12
    model = Article
    ordering = ["-date"]
    template_name = "news/news.html"
