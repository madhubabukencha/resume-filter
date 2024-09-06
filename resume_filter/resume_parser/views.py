# some_app/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = "resume_parser/parser_wrapper.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation to get the context
        context = super().get_context_data(**kwargs)
        
        # Add today's date and time to the context
        context['current_date'] = datetime.now().date()  # for date
        context['current_time'] = datetime.now().time()  # for time

        return context

