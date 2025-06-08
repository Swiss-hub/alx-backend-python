from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    # add other fields as needed

    def __str__(self):
        return self.name