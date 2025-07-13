import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
import requests
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCount
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import *

def index(request):
    popular_articles = HitCount.objects.all().order_by('-hits')
    # display 3 most popular articles published within the last 30 days
    popular_articles = [item.content_object for item in popular_articles if timezone.now() - item.content_object.date < datetime.timedelta(days=30)][:3]

    columns = Article.objects.filter(article_type="column").order_by("-date")[:2]
    interviews = Article.objects.filter(article_type="interview").order_by("-date")[:3]
    last_news = Article.objects.filter(article_type="news").order_by("-date")[:6]

    currency = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json").json()
    currency = {item["cc"]: round(item["rate"], 2) for item in currency if item["cc"] == "EUR" or item["cc"] == "USD"}

    enemy_losses_translation = {
        "personnel_units": _("Особовий склад"),
        "tanks": _("Танки"),
        "armoured_fighting_vehicles": _("ББМ"),
        "artillery_systems": _("Артилерія"),
        "mlrs": _("РСЗВ"),
        "aa_warfare_systems": _("ППО"),
        "planes": _("Літаки"),
        "helicopters": _("Гелікоптери"),
        "vehicles_fuel_tanks": _("Заправна техніка"),
        "warships_cutters": _("Кораблі"),
        "cruise_missiles": _("Крилаті ракети"),
        "uav_systems": _("БПЛА"),
    }
    enemy_losses = requests.get("https://russianwarship.rip/api/v2/statistics/latest").json()["data"]
    current_day_of_war = enemy_losses["day"]
    enemy_losses = [{"name": enemy_losses_translation[item], "losses_total": enemy_losses["stats"][item],
                     "losses_increase": enemy_losses["increase"][item], "img_name": f"{item}.png"} for item in
                    enemy_losses_translation]

    context = {
        "popular_articles": popular_articles,
        "columns": columns,
        "interviews": interviews,
        "last_news": last_news,
        "currency": currency,
        "enemy_losses": enemy_losses,
        "current_day_of_war": current_day_of_war
    }
    return render(request, "news/index.html", context)


@cache_page(60 * 15)
def article(request, article_title, article_id):
    article = get_object_or_404(Article, pk=article_id)
    tags = article.tags.all()
    recommendations = Article.objects.filter(tags__in=article.tags.all()).distinct().exclude(id=article_id).order_by("-date")[:3]

    # try to count hit
    hit_count = get_hitcount_model().objects.get_for_object(article)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    context = {
        "article": article,
        "recommendations": recommendations,
        "hits": hit_count.hits,
        "tags": tags
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


def search(request):
    context = {}
    if request.GET.get("search"):
        context["articles"] = Article.objects.filter(title__icontains=request.GET["search"])
    return render(request, "news/search.html", context)
