from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Set the default user ID here
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Todo(models.Model):
    project = models.ForeignKey(Project, related_name='todos', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.BooleanField(default=False)  # False for pending, True for completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description



# Create your models here.