from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control", "type":"text"}))
    date_start = forms.DateField(required=False, widget=forms.DateInput(attrs={"class":"form-control", "type":"date"}))
    date_stop = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))