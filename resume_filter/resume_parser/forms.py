from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    """
    This DocumentUploadForm will be passed to your template with
    your custom widgets.
    """
    class Meta:
        model = Document
        fields = ["file"]
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'file-input',  # Custom CSS class
                'id': 'file-upload',    # ID to match the label in your template
                'accept': '.pdf, .zip',  # You can also restrict file types
            }),
        }
