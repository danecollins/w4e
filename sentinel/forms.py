from django import forms
from sentinel.models import Sentinel



class SentinelAddForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Sentinel
        fields = ['name', 'tag', 'freq']
        widgets = {
            'name': forms.TextInput(attrs={'class': "large"}),
        }


class SentinelEditForm(forms.ModelForm):
    required_css_class = 'required'
    large = forms.TextInput(attrs={'class': "large"})
    class Meta:
        model = Sentinel
        fields = ['name', 'tag', 'freq', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': "large"}),
        }

