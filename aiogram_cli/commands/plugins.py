import typer

from aiogram_cli.loader import load_plugins_list


def plugins() -> None:
    """
    Get plugins list
    """
    for index, entry_point in enumerate(load_plugins_list(), start=1):
        typer.echo(f" {index}. {entry_point}")
