from django.db import models

# Create your models here.

import os
import uuid


def user_directory_path(instance, filename):
    # 随机生成新的图片名，自定义路径

    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:16], ext)
    sub_folder = 'file'
    if ext.lower() in ['jpg', 'png', 'gif']:
        sub_folder = 'pic/'
    if ext.lower() in ['pdf', 'docx']:
        sub_folder = 'document'
    return os.path.join(sub_folder, filename)


class PIC(models.Model):
    pic = models.ImageField(verbose_name="存放图片", upload_to=user_directory_path)
    md5 = models.CharField(verbose_name="md5值", max_length=128, unique=True)
    img_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'uploadImage'
