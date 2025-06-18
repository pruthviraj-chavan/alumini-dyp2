from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """Form for creating and updating posts"""
    class Meta:
        model = Post
        fields = ('title', 'category', 'content')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].help_text = "Text only content is allowed."
