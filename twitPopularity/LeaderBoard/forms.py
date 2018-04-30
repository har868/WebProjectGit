from .models import Person
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['Username', 'ScreenName', 'followers','following',]