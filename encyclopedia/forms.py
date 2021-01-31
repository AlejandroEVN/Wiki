# Form to use in 'new.html'
from django import forms

class Entry(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control col col-md-6 col-lg-8"}))
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control col col-md-6 col-lg-8", "rows": 10, "cols": 10}), required=True)