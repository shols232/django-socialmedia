from .models import Content, Comment
from django import forms
from django.core.exceptions import ValidationError
from .models import Content
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

class OgPostForm(forms.ModelForm):
    parent = Content()
    class Meta:
        model = Content
        fields = ('content','image_content', 'parent')

    # def clean(self):
    #     super(ContentForm, self).clean()
    #     console.log(self)
    #     content = self.cleaned_data.get('content')
    #     image_content = self.cleaned_data.get('image_content')
    #     if len(content) < 1 and image_content is None:
    #         self._errors['content'] = self.error_class([ 
    #             "Please post a content or an image or both"])
        # return self.cleaned_data

    def get_parent(self, value):
        return Content.objects.get(id=value.post_id)

    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =('content','image_content')