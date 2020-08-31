from django import forms
from .models import Comment


class NewCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = False
        self.fields['content'].widget.attrs.update({
            'placeholder': 'Your comment will go here...',
        })

    class Meta:
        model = Comment
        fields = ['content']
