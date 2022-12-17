from django.db import models

# Create your models here.
class UserInternetIession(models.Model):
    username = models.CharField(max_length=50)
    MAC = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    usage_time = models.TimeField()
    download = models.DecimalField(max_digits=12, decimal_places=2)
    upload = models.DecimalField(max_digits=12, decimal_places=2)