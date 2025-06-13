from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = CKEditor5Field(config_name="default")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    cover_image = ResizedImageField(size=[1500, 1000], crop=['middle', 'center'], upload_to="cover_image/")
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"title: {self.title}, author: {self.author}"
