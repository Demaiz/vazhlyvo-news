from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("title", "text")


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ("role",)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ("first_name", "last_name")