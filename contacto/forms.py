from django import forms

class ContactoForms(forms.Form):
    nombre = forms.CharField(label="Nombre", required=True, max_length=100)
    email = forms.EmailField(label="Email", required=True)
    contenido = forms.CharField(label="Contenido", widget=forms.Textarea)
