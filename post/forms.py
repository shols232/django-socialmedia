from .models import Content
from django import forms
class ContextForm(forms.ModelForm):
    """Form definition for Contextt."""

    class Meta:
        """Meta definition for Contactform."""

        model = Context
        fields = ('',)