from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """user learning topic"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        """return models char to display"""
        return self.text

class Entry(models.Model):
    """The sepecific knowledage that the user have masterred about one particular topic"""
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """the string will be displayed when return"""
        return self.text[:50] + "..."