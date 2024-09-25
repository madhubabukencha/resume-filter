# some_app/views.py
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Document
from .forms import DocumentUploadForm


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
