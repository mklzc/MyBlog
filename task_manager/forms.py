from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
        label="截止时间"
    )

    class Meta:
        model = Task
        fields = ['name', 'source', 'description', 'deadline']