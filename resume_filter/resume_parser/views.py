"""
Resume Parser Views
"""
import os
import csv
from openpyxl import Workbook
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from .models import Document, ProcessedDoc, ExtractedEntities
from .forms import DocumentUploadForm
from .help_functions import (extract_text_from_pdf,
                             extract_tables_from_pdf,
                             extract_entities_with_chatgpt)

# pylint: disable=no-member
# pylint: disable=unused-argument
# pylint: disable=too-many-ancestors


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
        # reverse returns absolute url by using name that
        # was need by get_success_url. You should not use
        # redirect here because it return Some HttpResponse that throws an
        # Error
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
    It is Delete view, Django asks you to create for all delete views
    """
    model = Document
    template_name = 'resume_parser/document_confirm_delete.html'
    # Redirects you after successful deletion
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
    - Also scheduled periodically using apscheduler
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


class ExtractedEntitiesListView(LoginRequiredMixin, ListView):
    """
    View to display and search extracted entities
    """
    model = ExtractedEntities
    template_name = 'resume_parser/extracted_info.html'
    # You will access data in the web template using this name
    context_object_name = 'entities_list'
    paginate_by = 4  # If you want to add pagination

    def get_queryset(self):
        """
        Optionally filter the queryset based on search input.
        """
        query = self.request.GET.get('q')
        queryset = ExtractedEntities.objects.filter(
            processed_doc__document__user=self.request.user
        )

        if query:
            reg_que = fr'\b{query}\b'
            queryset = queryset.filter(
              Q(processed_doc__document__original_filename__iregex=reg_que) |
              Q(processed_doc__document__unique_identifier__iregex=reg_que) |
              Q(skills__iregex=reg_que)
            )

        return queryset.order_by('-extracted_date')


def download_filtered_data(request):
    """
    Export filtered ExtractedEntities data to either CSV or Excel.
    Includes: unique_identifier, original_filename, and all fields
              from ExtractedEntities.
    """
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements
    # Filter queryset for the logged-in user and apply search filters
    query = request.GET.get('q')
    queryset = ExtractedEntities.objects.filter(
        processed_doc__document__user=request.user
    )

    if query:
        queryset = queryset.filter(
            Q(processed_doc__document__original_filename__icontains=query) |
            Q(processed_doc__document__unique_identifier__icontains=query) |
            Q(skills__icontains=query)
        )

    # Check the desired format from query parameters
    format_type = request.GET.get('format', 'csv').lower()  # Default to 'csv'

    if format_type == 'excel':
        # Create a workbook and a worksheet for Excel
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Extracted Entities"

        # Define Excel headers
        headers = [
            'Unique Identifier',
            'Original Filename',
            'Education Summary',
            'Work Experience Summary',
            'Overall Resume Summary',
            'Projects Summary',
            'Skills',
            'Contact Details',
            'Extracted Date'
        ]
        worksheet.append(headers)

        # Write the data rows
        for entity in queryset:
            unique_identifier = str(
                            entity.processed_doc.document.unique_identifier)
            original_filename = entity.processed_doc.document.original_filename
            education_summary = entity.education_summary
            work_experience_summary = entity.work_experience_summary
            overall_resume_summary = entity.overall_resume_summary
            projects_summary = entity.projects_summary
            skills = entity.skills
            contact_details = entity.contact_details
            # Format extracted_date to 'dd-mm-yyyy hh:mm:ss'
            extracted_date = entity.extracted_date
            if extracted_date:
                extracted_date = extracted_date.strftime('%d-%m-%Y %H:%M:%S')
            else:
                extracted_date = None

            worksheet.append([
                unique_identifier,
                original_filename,
                education_summary,
                work_experience_summary,
                overall_resume_summary,
                projects_summary,
                skills,
                contact_details,
                extracted_date,
            ])

        # Create the HttpResponse object for Excel
        con_type = "application/\
                    vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response = HttpResponse(content_type=con_type)
        cont_dis = 'attachment; filename="extracted_entities.xlsx"'
        response['Content-Disposition'] = cont_dis

        # Save the workbook to the response
        workbook.save(response)

    else:  # Default to CSV format
        # Create the HttpResponse object for CSV
        response = HttpResponse(content_type='text/csv')
        cont_dis = 'attachment; filename="extracted_entities.csv"'
        response['Content-Disposition'] = cont_dis

        # Write the CSV data
        writer = csv.writer(response)

        # Define CSV headers
        writer.writerow([
            'Unique Identifier',
            'Original Filename',
            'Education Summary',
            'Work Experience Summary',
            'Overall Resume Summary',
            'Projects Summary',
            'Skills',
            'Contact Details',
            'Extracted Date'
        ])

        # Write the data rows
        for entity in queryset:
            unique_identifier = str(
                entity.processed_doc.document.unique_identifier)
            original_filename = entity.processed_doc.document.original_filename
            education_summary = entity.education_summary
            work_experience_summary = entity.work_experience_summary
            overall_resume_summary = entity.overall_resume_summary
            projects_summary = entity.projects_summary
            skills = entity.skills
            contact_details = entity.contact_details
            # Format extracted_date to 'dd-mm-yyyy hh:mm:ss'
            extracted_date = entity.extracted_date
            if extracted_date:
                extracted_date = extracted_date.strftime('%d-%m-%Y %H:%M:%S')
            else:
                extracted_date = None

            writer.writerow([
                unique_identifier,
                original_filename,
                education_summary,
                work_experience_summary,
                overall_resume_summary,
                projects_summary,
                skills,
                contact_details,
                extracted_date,
            ])

    return response
