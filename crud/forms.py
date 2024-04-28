from django import forms
from .models import Task,Category

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'status','category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }
class TaskFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    # progress = forms.ChoiceField(choices=Task.PRIORITY_CHOICES, required=False)
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES, required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)