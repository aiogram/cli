from typing import Callable, Generator

import typer
from pkg_resources import EntryPoint, iter_entry_points
from typer import Typer


def load_plugins_list() -> Generator[EntryPoint, None, None]:
    yield from iter_entry_points(group="aiogram_cli.plugins", name=None)


def resolve_entry_point(app: Typer, entry_point: EntryPoint) -> None:
    plugin_loader: Callable[[Typer], None] = entry_point.resolve()
    plugin_loader(app)


def setup_plugins(app: Typer) -> None:
    for entry_point in load_plugins_list():
        try:
            resolve_entry_point(app=app, entry_point=entry_point)
        except Exception:
            typer.echo("Failed to load plugin {plugin}", err=True)
            raise
