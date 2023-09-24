from django.db import models
from django.contrib.auth.models import User



class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    collaborators = models.ManyToManyField(User, through='Collaboration', related_name='books_collaborated')


class Section(models.Model):
    title = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sections')
    parent_section = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='child_sections')


class Collaboration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'book']
