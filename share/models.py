from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class VideoInfo(models.Model):
    aws_file_name = models.CharField(max_length=256, verbose_name="AWSFilename", default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    download_count = models.IntegerField(verbose_name="Access Count", default=0)
    code = models.CharField(max_length=8, verbose_name="Code")
    upload_time = models.DateTimeField(default=datetime.now, verbose_name="Upload Time")
    download_path = models.CharField(max_length=256, verbose_name="Download Path")
    file_name = models.CharField(max_length=256, verbose_name="Filename", default="")
    file_size = models.CharField(max_length=10, verbose_name="File Size_KB")
    upload_ip = models.CharField(max_length=64, verbose_name="IP Address", default="")

    class Meta:
        verbose_name = "Video Information"
        db_table = "VideoInfo"

    def __str__(self): # the name we are going to see while query
        return self.file_name
