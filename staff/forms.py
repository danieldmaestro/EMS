from django import forms
from django.core.exceptions import ValidationError
from .models import Query

class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    def clean_image(self):
        profile_picture = self.cleaned_data['profile_picture']
        if profile_picture.size > 2000000:
            raise ValidationError('Image file is too large (max 2MB).')
        if not profile_picture.content_type in ['image/jpeg', 'image/png']:
            raise ValidationError('Image file must be JPEG or PNG.')
        return profile_picture
    
class QueryResponseForm(forms.ModelForm):
    response = forms.CharField(
        label='Response to for Query',
        max_length=300,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Your Response to the query here'}),
    )
    """Form for query response"""
    class Meta:
        model = Query
        fields = ['response',]
