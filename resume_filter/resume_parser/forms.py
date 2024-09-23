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
                # ID to match the label in your template
                'id': 'file-upload',
                # You can also restrict file types
                # in future add ',zip' to take zip files as input
                'accept': '.pdf',
            }),
        }
