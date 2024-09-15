# some_app/views.py
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Document
from .forms import DocumentUploadForm
from django.contrib import messages


class AboutView(LoginRequiredMixin, CreateView):
    """
    View for Document upload
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
        It will redirect to specified resume-filter-home once
        document is uploaded
        """
        return reverse('resume-filter-home')


# class DocumentListView(LoginRequiredMixin, ListView):
#     model = Document
#     template_name = 'resume_parser/list.html'

#     def get_queryset(self):
#         return Document.objects.filter(user=self.request.user)
