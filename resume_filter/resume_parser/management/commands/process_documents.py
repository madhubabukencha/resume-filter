"""
If you have a piece of code that you want to execute manually or
by using cron syntax you can create this kind of Command files.
We are creating this file to process pdf documents manually.

This file executes when you run:
python manage.py process_documents
"""
from django.core.management.base import BaseCommand
from resume_parser.views import process_documents


class Command(BaseCommand):
    help = 'Process unprocessed documents and update status'

    def handle(self, *args, **kwargs):
        """
        This method is called when the command is executed.
        """
        process_documents(None)
        self.stdout.write(self.style.SUCCESS('Successfully processed unprocessed documents'))
