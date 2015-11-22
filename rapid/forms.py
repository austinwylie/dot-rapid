from django import forms


class UploadFileForm(forms.Form):
    des = forms.CharField(max_length=50, label='Description ')
    public = forms.BooleanField(initial=False, required=False)
    token = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'style' : 'display: none'}))
    file = forms.FileField(label='File ')
