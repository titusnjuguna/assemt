from django import forms

class CSVUploadForm(forms.Form):
    source_file = forms.FileField(label="SourceFile", required=True)
    target_file = forms.FileField(label="TargetFile", required=True)
