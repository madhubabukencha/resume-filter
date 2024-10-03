from django.apps import AppConfig
from django.db import connections, OperationalError
from django.db.migrations.executor import MigrationExecutor


class ResumeParserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resume_parser'

    def ready(self) -> None:
        # Ensure that the database is migrated
        # If you run without DB check, you might get some db not found error
        if self._is_db_synchronized():
            from . import signals
            from . import jobs
            jobs.start_scheduler()

    def _is_db_synchronized(self):
        """Check if all migrations have been applied."""
        db_conn = connections['default']
        try:
            # Check if the database connection is available
            db_conn.ensure_connection()
            executor = MigrationExecutor(db_conn)
            # If there's any unapplied migration, it returns False
            return not executor.migration_plan(
                                executor.loader.graph.leaf_nodes())
        except OperationalError:
            # If there's an operational error, migrations likely haven't run
            print("Database is unavailable. Scheduler will not start.")
            return False
