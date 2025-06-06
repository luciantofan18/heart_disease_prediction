from django import forms
from .models import Pacient
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ParamConsult
from .models import PacientFile

class PacientForm(forms.ModelForm):
    class Meta:
        model = Pacient
        fields = ['nume', 'prenume', 'birth_date', 'sex', 'email']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    upload_document = forms.FileField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','upload_document']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

from django import forms
from .models import ParamConsult

class ParamConsultForm(forms.ModelForm):
    class Meta:
        model = ParamConsult
        exclude = ['age', 'sex', 'doctor', 'pacient', 'data', 'Verified', 'Risk']
        widgets = {
            'RestingBP': forms.NumberInput(attrs={'placeholder': '0 - 200'}),
            'Cholesterol': forms.NumberInput(attrs={'placeholder': '0 - 600'}),
            'FastingBS': forms.NumberInput(attrs={'placeholder': '0 - 250'}),
            'MaxHR': forms.NumberInput(attrs={'placeholder': '30 - 250'}),
            'Oldpeak': forms.NumberInput(attrs={'placeholder': '-4.0 – 7.0'}),
        }


    def __init__(self, *args, **kwargs):
        super(ParamConsultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = False


class PacientFileForm(forms.ModelForm):
    class Meta:
        model = PacientFile
        fields = ['uploaded_file']
