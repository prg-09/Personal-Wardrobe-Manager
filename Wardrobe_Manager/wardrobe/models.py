from django.db import models
from django.contrib.auth.models import User

class Clothitem(models.Model):
    name = models.CharField(max_length = 100)
    category = models.CharField (max_length = 100)
    season = models.CharField(max_length = 100)
    photo = models.ImageField(upload_to = 'clothes/')
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.name
    
class Outfit (models.Model):
    name = models.CharField (max_length = 100)
    items = models.ManyToManyField(Clothitem)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)




