from django.db import models
from django.contrib.auth.models import User
import uuid


# HELP FUNCTIONS
def user_directory_path(instance, filename):
    """
    This function create a directory with username inside document 
    directory. Inside username directory you will find your uploaded file.
    """
    return f'documents/{instance.user.username}/{filename}'


# Create your models here.
class Document(models.Model):
    """
    Model for Document upload
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name}"
