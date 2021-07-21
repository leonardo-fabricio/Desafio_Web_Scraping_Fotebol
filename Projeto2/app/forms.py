from django import forms
from django.db.models import fields
from .models import Time

class TimeForm(forms.Form):
    nome = forms.CharField(label='Nome')
    sigla = forms.CharField(label='Sigla')
    serie = forms.CharField(label='Serie')

    def send(self):
        nome = self.cleaned_data['nome']
        sigla = self.cleaned_data['sigla']
        serie = self.cleaned_data['serie']

class TimesModel(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['nome','sigla','serie']