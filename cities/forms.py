from django import forms
from cities.models import City


class HomeCityForm(forms.Form):
    name = forms.CharField(label='Город', max_length=20)


class CityForm(forms.ModelForm):
    name = forms.CharField(label='Город', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите название города'
    }))

    class Meta:
        model = City
        fields = ('name', )
