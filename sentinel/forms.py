from __future__ import print_function
from __future__ import unicode_literals

from django import forms
from sentinel.models import Sentinel, ContactInfo
import sys


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


class ContactInfoForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = ContactInfo
        fields = ['contact_by', 'email', 'number']
        labels = {
            'number': ('Used for SMS only')
        }

    def clean_number(self):
        n = self.cleaned_data['number']
        print(n, file=sys.stderr)
        # string is unicode so translate works differently
        n = n.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        print(n, file=sys.stderr)
        if n.startswith('+1'):
            if len(n) == 12:
                # probably a good number
                print(n, file=sys.stderr)
                n = "+1({}) {}-{}".format(n[2:5], n[5:8], n[8:])
            else:
                raise forms.ValidationError('Number starts with +1 but does not have 10 other digits')
        else:
            if len(n) == 10:
                # probably a good number
                n = "+1" + n
                print(n, file=sys.stderr)
                n = "+1({}) {}-{}".format(n[2:5], n[5:8], n[8:])
            else:
                raise forms.ValidationError('Number does not have 10 other digits')

        return n


class BetaForm(forms.Form):
    required_css_class = 'required'
    first_name = forms.CharField(label='First Name', max_length=40, required=True)
    last_name = forms.CharField(label='Last Name', max_length=50, required=True)
    email = forms.EmailField()
    company = forms.CharField(label='Company', max_length=50, required=True)
