from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    fields = ["title", "text", "cover_image", "tags", "article_type"]

    # set current user as article author
    def save_model(self, request, obj, form, change):
        obj.author = Author.objects.get(user=request.user)
        super().save_model(request, obj, form, change)

    # return only current user's articles; return all if superuser
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(author__user=request.user)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Tag)
