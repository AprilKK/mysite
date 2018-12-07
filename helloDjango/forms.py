from django import forms

class UploadFileForm(forms.Form):
    AritcalTitle = forms.CharField(max_length = 100)
    ArticalSubtitle = forms.CharField(max_length =200)
    AritcalAbstract = forms.CharField(max_length = 800)
    ArticalFileUpload = forms.FileField()