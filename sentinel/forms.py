from django import forms
from sentinel.models import Sentinel



class SentinelAddForm(forms.ModelForm):
    class Meta:
        model = Sentinel
        fields = ['name', 'tag', 'freq']
        labels = {
            'name': ('Name (required)'),
            'freq': ('Frequency (required)')
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "large"}),
            'tag': forms.TextInput(attrs={'hidden': True})
        }


class SentinelEditForm(forms.ModelForm):
    required_css_class = 'required'
    large = forms.TextInput(attrs={'class': "large"})
    class Meta:
        model = Sentinel
        fields = ['name', 'freq', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': "large"}),
        }

