import aiogram
import typer

import aiogram_cli


def version() -> None:
    typer.echo(f"aiogram-cli: v{aiogram_cli.__version__}")
    typer.echo(f"aiogram: v{aiogram.__version__}")
