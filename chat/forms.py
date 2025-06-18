from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """Form for sending messages"""
    class Meta:
        model = Message
        fields = ('message_text',)
        widgets = {
            'message_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }
        labels = {
            'message_text': '',
        }
