from django import forms
from .models import *

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    phone = forms.CharField(label='Your Phone', max_length=20)
    message = forms.CharField(label='Your Message', widget=forms.Textarea)





class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'email', 'resume', 'cover_letter']


class DynamicURLData(forms.Form):
	class meta:
		model = DynamicURL
		fields = '__all__'
            

from django import forms
from .models import PackageDownload

class PackageDownloadForm(forms.ModelForm):
    class Meta:
        model = PackageDownload
        fields = ['name', 'email', 'phone', 'looking_for', 'message']
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '10-Digit Phone Number', 'class': 'form-input', 'pattern': '[0-9]*', 'inputmode': 'numeric'}),
            'looking_for': forms.Select(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Any specific requirements...', 'rows': 3, 'class': 'form-input'}),
        }