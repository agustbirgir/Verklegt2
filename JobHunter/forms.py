from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone_number', 'street_name', 'house_number', 'postal_code', 'country', 'profile_image']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'street_name', 'house_number', 'postal_code', 'country', 'bio']