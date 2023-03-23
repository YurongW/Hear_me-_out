from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# Create your models here.
def pic_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return f"media/{instance.id}/{filename}"


class Account(AbstractUser):
    avatar = models.URLField(verbose_name="customer avatar", default="/media/pic/default.jpg")
    is_deleted = models.BooleanField(default=False, verbose_name="is deleted")
    num_post = models.IntegerField(default=0)
    num_like = models.IntegerField(default=0)
