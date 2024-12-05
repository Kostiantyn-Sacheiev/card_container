import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

from app import app, db
from app.models import User, Card

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Set the target metadata to use the metadata from your db instance.
target_metadata = db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not url:
        raise ValueError("Database URL not found in app configuration.")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        version_table_schema='public',
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    # Ensure that the application context is available
    with app.app_context():
        connectable = db.engine

        # Define the process_revision_directives callback
        def process_revision_directives(context, revision, directives):
            if getattr(config.cmd_opts, 'autogenerate', False):
                script = directives[0]
                if script.upgrade_ops.is_empty():
                    directives[:] = []
                    logger.info('No changes in schema detected.')

        conf_args = current_app.extensions['migrate'].configure_args
        if conf_args.get("process_revision_directives") is None:
            conf_args["process_revision_directives"] = process_revision_directives

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                version_table_schema='public',
                **conf_args
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
