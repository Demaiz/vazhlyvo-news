from django import forms
from django.utils.translation import gettext_lazy as _

class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control", "type":"text", "placeholder": _("Search")}))
    date_start = forms.DateField(required=False, label=_("From"), widget=forms.DateInput(attrs={"class":"form-control", "type":"date"}))
    date_stop = forms.DateField(required=False, label=_("To"), widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))