from .models import Content, Comment
from django import forms
from django.core.exceptions import ValidationError
class ContentForm(forms.ModelForm):
    """Form definition for Contextt."""

    class Meta:
        """Meta definition for Contactform."""
        model = Content
        fields = ('content','image_content')

    def clean(self):
        super(ContentForm, self).clean()
        content = self.cleaned_data.get('content')
        image_content = self.cleaned_data.get('image_content')
        if len(content) < 1 and image_content is None:
            self._errors['content'] = self.error_class([ 
                "Please post a content or an image or both"])
        return self.cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =('content','image_content')