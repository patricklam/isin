from django.db import models

class Status(models.Model):
  status = models.CharField(max_length=80)
  pub_date = models.DateTimeField('update date')
  image = models.ImageField(upload_to='in-imgs')
