from django.apps import AppConfig


class ResumeParserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resume_parser'

    def ready(self) -> None:
        # All below import functions runs when you run server
        from . import signals
        from . import jobs
        jobs.start_scheduler()

