from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            