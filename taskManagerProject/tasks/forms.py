from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title', 'desc', 'importance')
        #exclude = ('createDate', 'completeDate', 'user')
        #fields = '__all__'
