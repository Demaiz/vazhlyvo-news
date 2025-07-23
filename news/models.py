from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name=_("User"))
    photo = ResizedImageField(size=[400, 400], crop=['middle', 'center'], upload_to="author_photo/", verbose_name=_("Photo"))
    role = models.CharField(max_length=130, verbose_name=_("Role"))

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Article(models.Model):
    TYPE_CHOICES = [
        ("news", _("news")),
        ("column", _("column")),
        ("interview", _("interview"))
    ]
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    text = models.TextField(verbose_name=_("Text"))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Author"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    cover_image = ResizedImageField(size=[1500, 1000], crop=['middle', 'center'], upload_to="cover_image/", verbose_name=_("Image"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))
    article_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name=_("Article type"))

    def __str__(self):
        return f"'{self.title}' {_("by")} {self.author}"


    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
