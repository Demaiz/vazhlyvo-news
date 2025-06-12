from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = CKEditor5Field(config_name="default")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title: {self.title}, author: {self.author}"
