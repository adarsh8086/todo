from django import forms
from .models import Project, Todo

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['description', 'status']
