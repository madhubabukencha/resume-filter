from django.apps import AppConfig


class ResumeParserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resume_parser'

    def ready(self) -> None:
        # import all your signal files here
        from . import signals


