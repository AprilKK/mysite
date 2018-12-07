from django import forms

class UploadFileForm(forms.Form):
    ArticalTitle = forms.CharField(max_length = 100)
    ArticalSubtitle = forms.CharField(max_length =200)
    ArticalAbstract = forms.CharField(max_length = 800)
    ArticalFileUpload = forms.FileField()
