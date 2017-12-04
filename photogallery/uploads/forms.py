from django import forms

from .models import Post

class DeleteNewForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []