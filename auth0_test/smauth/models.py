from django.db import models


# Create your models here.
class Token(models.Model):
    uid = models.CharField(max_length=255, primary_key=True)
    access_token = models.CharField(max_length=255)
    expires = models.DateTimeField()
    token_type = models.CharField(max_length=255)
