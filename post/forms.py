from .models import Content
from django import forms
class ContentForm(forms.ModelForm):
    """Form definition for Contextt."""

    class Meta:
        """Meta definition for Contactform."""

        model = Content
        fields = ('content','image_content')