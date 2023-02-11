from django.db import models
from django.contrib.auth.models import User

LANG_CHOICE = (
    ('py', 'Python'),
    ('js', 'JavaScript'),
    ('cpp', 'C++')
)

PRIVACY_CHOICE = (
    (False, 'Публичный'),
    (True, 'Частный')
)


class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG_CHOICE)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
    privacy = models.BooleanField(choices=PRIVACY_CHOICE)

    # class Meta:
    #     ordering = ["name", "creation_date"]


class Comment(models.Model):
   text = models.TextField(max_length=1000)
   creation_date = models.DateTimeField(auto_now=True)
   author = models.ForeignKey(to=User, on_delete=models.CASCADE)
   snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, related_name='comments')
