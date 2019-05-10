from django.db import models


# Create your models here.
class Token(models.Model):
    uid = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    expires_in = models.DateField()
    token_type = models.CharField(max_length=255)
