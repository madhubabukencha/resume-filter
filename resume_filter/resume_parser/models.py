"""This contains all user defined models.
A model is nothing but a table.
"""
import uuid
from django.db import models
from django.contrib.auth.models import User


# HELP FUNCTIONS
def user_directory_path(instance, filename):
    """
    Save the file with a unique identifier in the username's directory.
    """
    # Generate a unique file name by appending the UUID before
    # the file extension
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{extension}"
    return f'{instance.user.username}/{new_filename}'


class Document(models.Model):
    """
    Model for Document upload
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    # Store the original file name
    original_filename = models.CharField(max_length=255)
    status = models.CharField(max_length=30, default="unprocessed")

    def __str__(self):
        return self.original_filename  # Display original file name

    def save(self, *args, **kwargs):
        # If this is a new file upload (i.e., no existing file),
        # store the original file name
        if not self.pk:
            self.original_filename = self.file.name

        super().save(*args, **kwargs)


class ProcessedDoc(models.Model):
    """
    Model to store processed document data.
    """
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    extracted_text = models.TextField()
    extracted_tables = models.TextField()
    processed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # pylint: disable=no-member
        return f"Processed: {self.document.original_filename}"


class ExtractedEntities(models.Model):
    """
    Model to store the extracted resume data.
    Each record corresponds to a single document.
    """
    processed_doc = models.OneToOneField(ProcessedDoc, on_delete=models.CASCADE)
    education_summary = models.TextField(null=True, blank=True)
    work_experience_summary = models.TextField(null=True, blank=True)
    overall_resume_summary = models.TextField(null=True, blank=True)
    projects_summary = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    contact_details = models.TextField(null=True, blank=True)
    extracted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entities for: {self.processed_doc.document.original_filename}"
