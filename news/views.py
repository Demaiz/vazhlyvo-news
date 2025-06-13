from django.shortcuts import render
from .models import *

def index(request):
    context = {
        "articles": Article.objects.all().values()
    }
    return render(request, "news/index.html", context)
