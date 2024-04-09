"""
https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/#django.forms.ModelForm
"""

from django import forms
from django.forms import ModelForm
from weblink.models import User, Link, Tag

class ProfileUpdateForm(ModelForm):
     class Meta:
         model = User
         fields = ["email", "first_name", "last_name", "email"]

# MultipleChoiceField
# https://docs.djangoproject.com/en/5.0/ref/forms/fields/#modelmultiplechoicefield
tag_q = Tag.objects.all()

class FavoriteLinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ["url_text", "category"]
    url_text = forms.URLField(widget=forms.URLInput)
    tag_select = forms.ModelMultipleChoiceField(queryset=tag_q, required=False)

class UpdateLinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ["url_text", "title", "category"]
    tag_select = forms.ModelMultipleChoiceField(queryset=tag_q)


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)