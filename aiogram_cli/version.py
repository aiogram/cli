import aiogram
import click

from aiogram_cli import __version__


@click.command("version")
def command_version():
    """Get an application version"""
    click.echo(f"aiogram-cli: v{__version__}")
    click.echo(f"aiogram: v{aiogram.__version__}")
