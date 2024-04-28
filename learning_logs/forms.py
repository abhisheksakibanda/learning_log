"""
Forms for the learning_logs app.
"""
from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """
    Form for creating a new topic.
    """
    class Meta:
        """
        Meta class for TopicForm.
        """
        model = Topic
        fields = ['text', 'public']
        labels = {'text': '', 'public': 'Make Public'}
        public = forms.BooleanField(required=False)


class EntryForm(forms.ModelForm):
    """
    Form for creating a new entry.
    """
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
