"""
Resume Parser Views
"""
import os
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from .models import Document, ProcessedDoc, ExtractedEntities
from .forms import DocumentUploadForm
from .help_functions import (extract_text_from_pdf,
                             extract_tables_from_pdf,
                             extract_entities_with_chatgpt)

# pylint: disable=no-member
# pylint: disable=unused-argument


class DocumentUploadView(LoginRequiredMixin, CreateView):
    """
    View for uploading document
    """
    model = Document
    form_class = DocumentUploadForm
    template_name = "resume_parser/upload_docs.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Document is uploaded successfully!!")
        return response

    def get_success_url(self):
        """
        It will redirect to resume-filter-home once document is uploaded
        """
        return reverse('resume-filter-home')


class DocumentListView(LoginRequiredMixin, ListView):
    """
    It will list the uploaded documents
    """
    model = Document
    template_name = 'resume_parser/uploaded_docs.html'

    def get_queryset(self):
        # -uploaded_date: The minus sign (-) before the field name orders the
        #  queryset in descending order. Without the minus sign, it would be in
        # ascending order (oldest to newest).
        return Document.objects.filter(
               user=self.request.user).order_by('-uploaded_date')


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    """
    It is Delete view
    """
    model = Document
    template_name = 'resume_parser/document_confirm_delete.html'
    success_url = reverse_lazy('uploaded-docs')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Document has been deleted.")
        return super().delete(request, *args, **kwargs)


def process_documents(request):
    """
    Process unprocessed documents and store extracted data.

     This function executes,
    - When you run a command:
      `python manage.py process_documents`
    - Also schedule periodically using apscheduler
    """
    unprocessed_docs = Document.objects.filter(status='unprocessed')

    for document in unprocessed_docs:
        if document.file.name.endswith('.pdf'):
            file_path = document.file.path
            base_file_name = os.path.basename(file_path)
            print(f"Started Processing: {base_file_name}")

            extracted_text = extract_text_from_pdf(file_path)
            extracted_tables = extract_tables_from_pdf(file_path)
            print(f"{base_file_name} processing is done")

            # Using atomic transaction to prevent race conditions
            # and ensure integrity
            with transaction.atomic():
                # Lock the document record to prevent duplicates during
                # concurrent processing
                document = Document.objects.select_for_update().get(
                           pk=document.pk)

                # Check if the document already has a processed record
                processed_doc, created = ProcessedDoc.objects.get_or_create(
                    document=document,
                    defaults={
                        'extracted_text': extracted_text,
                        'extracted_tables': extracted_tables,
                    }
                )

                if not created:
                    # If already exists, update the existing record
                    processed_doc.extracted_text = extracted_text
                    processed_doc.extracted_tables = extracted_tables
                    processed_doc.save()

            print(f"Storing data in ProcessedDoc table for: {base_file_name}")

            # Now extract entities using the ChatGPT API
            response = extract_entities_with_chatgpt(extracted_text,
                                                     extracted_tables)
            print(f"Extracting Entities for {base_file_name}")
            # Update or create ExtractedEntities
            ExtractedEntities.objects.update_or_create(
                processed_doc=processed_doc,
                defaults={
                    'education_summary': response.get("education-summary"),
                    'work_experience_summary': response.get(
                                               "work-experience-summary"),
                    'overall_resume_summary': response.get(
                                              "overall-resume-summary"),
                    'projects_summary': response.get("projects-summary"),
                    'skills': response.get("skills"),
                    'contact_details': response.get("contact-details")
                }
            )
            print("Extracting Entities is done")

            # Mark the document as processed
            document.status = 'processed'
            document.save()
    return "Documents processed successfully."
