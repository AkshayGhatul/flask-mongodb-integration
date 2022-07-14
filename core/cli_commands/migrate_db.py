import click
from flask import Flask
from flask import current_app
from core.migrations import MigrationUtils

@current_app.cli.command("migrate")
@click.option('--version', required=True, type=int)
def migrate_db(version):
    MigrationUtils.migrate(version)