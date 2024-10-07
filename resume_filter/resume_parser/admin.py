'''
Whatever models you register here, you will be able to see them
in Django database UI.
'''
from django.contrib import admin
from .models import Document, ProcessedDoc, ExtractedEntities


# Register your models here so that so will appear in your db.
admin.site.register(Document)
admin.site.register(ProcessedDoc)
admin.site.register(ExtractedEntities)
