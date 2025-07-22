from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from hitcount.admin import HitCountAdmin
from hitcount.models import HitCount, Hit
from modeltranslation.admin import TranslationAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin


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

    # also delete related hitcount object
    def delete_model(self, request, obj):
        HitCount.objects.filter(object_pk=obj.id).delete()
        super().delete_model(request, obj)

    # also delete each related hitcount object in the queryset
    def delete_queryset(self, request, queryset):
        for article in queryset:
            HitCount.objects.filter(object_pk=article.id).delete()
        super().delete_queryset(request, queryset)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Tag)
# unregister and register the User model to add translation fields to the admin panel
admin.site.unregister(User)
admin.site.register(User)

# remove Hit model from the admin panel
admin.site.unregister(Hit)
