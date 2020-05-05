from typer import Typer

from aiogram_cli.commands.plugins import plugins
from aiogram_cli.commands.version import version


def setup(app: Typer) -> None:
    app.command()(plugins)
    app.command()(version)
