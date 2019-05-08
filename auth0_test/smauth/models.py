from django.db import models


# Create your models here.
class Token(models.Model):
    access_token = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    expires_in = models.DateField()
    token_type = models.CharField(max_length=255)
