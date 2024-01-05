from django import forms
from .models import Posts, Response
from ckeditor_uploader.fields import RichTextUploadingFormField


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['category', 'headline', 'text']
        widgets = {'to_reg_user': forms.HiddenInput()}


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {'res_user': forms.HiddenInput()}


# class CkEditorForm(forms.Form):
#     ckeditor_standard_field = RichTextField()
#     ckeditor_uploader_field = RichTextUploadingFormField()
