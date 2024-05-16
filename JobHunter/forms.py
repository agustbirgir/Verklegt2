from django import forms
from .models import Profile




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone_number', 'street_name', 'house_number', 'postal_code', 'city', 'country', 'profile_image']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'street_name', 'house_number', 'postal_code', 'city', 'country', 'bio']

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if not bio:
            raise forms.ValidationError("This field cannot be empty.")
        return bio



    def clean_street_name(self):
        street_name = self.cleaned_data.get('street_name')
        if not street_name:
            raise forms.ValidationError("This field cannot be empty.")
        return street_name

    def clean_house_number(self):
        house_number = self.cleaned_data.get('house_number')
        if not house_number:
            raise forms.ValidationError("This field cannot be empty.")
        return house_number

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code:
            raise forms.ValidationError("This field cannot be empty.")
        return postal_code

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError("This field cannot be empty.")
        return country

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError("This field cannot be empty.")
        return city

