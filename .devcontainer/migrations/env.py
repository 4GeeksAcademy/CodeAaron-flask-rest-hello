# migrations/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from alembic.runtime.migration import MigrationContext
from alembic.autogenerate import produce_migrations, compare_metadata
from src.models import Base  # Ensure correct import path to your models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Retrieve the database URL from the environment variable
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL environment variable set")

config.set_main_option('sqlalchemy.url', DATABASE_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    # Read the SQLAlchemy URL from the Alembic config
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = config.get_main_option("sqlalchemy.url")
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Enable comparison of column types
            compare_server_default=True  # Enable comparison of server defaults
        )

        # Create a migration context to produce migrations
        migration_context = MigrationContext.configure(connection)
        diff = produce_migrations(migration_context, target_metadata)
        if not diff.upgrade_ops.is_empty():
            context.run_migrations()
        else:
            print("No changes in schema detected. An empty migration version file will be created under ./migrations/versions/ directory")


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
