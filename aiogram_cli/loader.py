from typing import Any, Callable, Generator, Sequence, Type, Union

from cleo import Application, Command
from pkg_resources import EntryPoint, iter_entry_points

CommandType = Union[Command, Type[Command]]
CommandLoaderType = Callable[[Application], Union[CommandType, Sequence[CommandType]]]
CommandExtension = Union[CommandType, CommandLoaderType]

EXTENSIONS_GROUP = "aiogram_cli.plugins"


class ExtensionsLoader:
    def __init__(self, group: str = EXTENSIONS_GROUP) -> None:
        self.group = group

    def iter_entry_points(self) -> Generator[EntryPoint, None, None]:
        yield from iter_entry_points(group=self.group, name=None)

    def resolve_entry_points(self) -> Generator[Any, None, None]:
        for entry_point in self.iter_entry_points():
            yield entry_point.resolve()

    def _load_plugin(self, plugin: Any, app: Application) -> Generator[Command, None, None]:
        if isinstance(plugin, Command):
            yield plugin
        elif issubclass(plugin, Command):
            yield plugin()
        elif isinstance(plugin, Sequence):
            for item in plugin:
                yield from self._load_plugin(item, app=app)
        elif callable(plugin):
            plugin = plugin(app)
            yield from self._load_plugin(plugin, app=app)
        else:
            raise TypeError(f"{plugin} is not Command or factory")

    def _resolve_plugins(self, app: Application) -> Generator[Command, None, None]:
        for plugin in self.resolve_entry_points():
            yield from self._load_plugin(plugin, app=app)

    def setup(self, app: Application) -> None:
        for command in self._resolve_plugins(app):
            app.add(command)
