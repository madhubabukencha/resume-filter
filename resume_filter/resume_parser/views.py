"""
Resume Parser Views
"""
import os
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Document, ProcessedDoc
from .forms import DocumentUploadForm
from .help_functions import (extract_text_from_pdf,
                             extract_tables_from_pdf)


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
        return Document.objects.filter(user=self.request.user).order_by('-uploaded_date')


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'resume_parser/document_confirm_delete.html'
    success_url = reverse_lazy('uploaded-docs')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Document has been deleted.")
        return super().delete(request, *args, **kwargs)


def process_documents(request):
    """
    Find unprocessed documents, extract data, and mark them as processed.

    This function executes,
    - When your run a below command:
      `python manage.py process_documents`
    - Also schedule periodically using apscheduler
    """
    unprocessed_docs = Document.objects.filter(status='unprocessed')

    for document in unprocessed_docs:
        # # If the file is a ZIP, unzip and process its contents
        # if document.file.name.endswith('.zip'):
        #     process_zip_file(document)
        if document.file.name.endswith('.pdf'):
            # Process a single PDF file
            file_path = document.file.path
            base_file_name = os.path.basename(file_path)
            print(f"Started Processing: {base_file_name}")
            extracted_text = extract_text_from_pdf(file_path)
            extracted_tables = extract_tables_from_pdf(file_path)
            print(f"{base_file_name} processing is done")

            # Create a ProcessedDocument entry
            ProcessedDoc.objects.create(
                document=document,
                extracted_text=extracted_text,
                extracted_tables=extracted_tables,
            )

            # Mark document as processed
            document.status = 'processed'
            document.save()

            # Send email for a single processed document
            # send_processing_email(document.user.email, [document.original_filename])

    return "Documents processed successfully."
