from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo = ResizedImageField(size=[400, 400], crop=['middle', 'center'], upload_to="author_photo/")
    role = models.CharField(max_length=130)

    def __str__(self):
        return self.user.__str__()


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    TYPE_CHOICES = [
        ("news", _("news")),
        ("column", _("column")),
        ("interview", _("interview"))
    ]
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    cover_image = ResizedImageField(size=[1500, 1000], crop=['middle', 'center'], upload_to="cover_image/")
    tags = models.ManyToManyField(Tag, blank=True)
    article_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"title: {self.title}, author: {self.author}"
