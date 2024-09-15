"""
To make this signal file work you have to import this file
apps.py file
"""
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Document
import os

@receiver(post_delete, sender=Document)
def delete_file_on_model_delete(sender, instance, **kwargs):
    """
    Deletes the file from the filesystem when the corresponding 
    `Document` object is deleted.
    """
    if instance.file:
        file_path = instance.file.path
        if os.path.isfile(file_path):
            os.remove(file_path)