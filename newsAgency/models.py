from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   name = models.CharField(max_length=64)

   def __str__(self):
      return self.name

class Story(models.Model):
   author = models.ForeignKey(Author, on_delete=models.CASCADE)
   headline = models.CharField(max_length=64)
   CATEGORY_CHOICES = (
      ('pol', 'politics'),
      ('art', 'art'),
      ('tec', 'technology'),
      ('trivia', 'trivial news'),
   )
   category = models.CharField(max_length=6, choices=CATEGORY_CHOICES)
   REGION_CHOICES = (
      ('uk', 'United Kingdom'),
      ('eu', 'European Union'),
      ('w', 'World')
   )
   region = models.CharField(max_length=2, choices=REGION_CHOICES)
   details = models.CharField(max_length=512)
   pub_date = models.DateTimeField('date published')
   
   def __str__(self):
      return self.headline
