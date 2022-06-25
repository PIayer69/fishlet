from django.db import models
from model_utils import FieldTracker
from django.contrib.auth.models import User

# Create your models here.

class Set(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    tracker = FieldTracker()


    def __str__(self):
        return f'{self.user} set: {self.name}'

    class Meta:
        ordering = ['-updated', '-created']
    


class Question(models.Model):
    question_set = models.ForeignKey(Set, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    definition = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    tracker = FieldTracker()
    
    def __str__(self):
        return f'{self.question_set.name} : {self.name}'