from django.db import models
from django.contrib.auth.models import User
import uuid


# HELP FUNCTIONS
def user_directory_path(instance, filename):
    """
    Save the file with a unique identifier in the username's directory.
    """
    # Generate a unique file name by appending the UUID before the file extension
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{extension}"
    return f'documents/{instance.user.username}/{new_filename}'


class Document(models.Model):
    """
    Model for Document upload
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255)  # Store the original file name

    def __str__(self):
        return self.original_filename  # Display original file name

    def save(self, *args, **kwargs):
        # If this is a new file upload (i.e., no existing file), store the original file name
        if not self.pk:
            self.original_filename = self.file.name

        super().save(*args, **kwargs)
