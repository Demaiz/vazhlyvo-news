from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from modeltranslation.admin import TranslationAdmin
from .models import *


class ArticleAdmin(TranslationAdmin):
    fields = ["title", "text", "cover_image", "tags", "article_type"]

    # display CKEditor5Widget instead of TextField
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget},
    }

    # set current user as article author
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.author = Author.objects.get(user=request.user)
        super().save_model(request, obj, form, change)

    # return only current user's articles; return all if superuser
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(author__user=request.user)

    # display author field only for superusers
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.is_superuser and "author" not in fields:
            fields.append("author")
        return fields

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Tag)
