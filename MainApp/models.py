from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

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
    creation_date = models.DateTimeField(default=now, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
    privacy = models.BooleanField(choices=PRIVACY_CHOICE)
    rating = models.IntegerField(default=0)
    voted = models.TextField(max_length=5000, default='')

    # class Meta:
    #     ordering = ["name", "creation_date"]

    def __str__(self):
        return f"Snippet {self.name} / {self.user}"

class Comment(models.Model):
   def validate_image(fieldfile_obj):
       filesize = fieldfile_obj.file.size
       megabyte_limit = 1.0
       if filesize > megabyte_limit * 1024 * 1024:
           raise ValidationError("Image file too large ( > 1mb )")

   text = models.TextField(max_length=1000)
   creation_date = models.DateTimeField(auto_now=True)
   author = models.ForeignKey(to=User, on_delete=models.CASCADE)
   snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, related_name='comments')
   image = models.ImageField(upload_to="images/", null=True, blank=True, validators=[validate_image])

