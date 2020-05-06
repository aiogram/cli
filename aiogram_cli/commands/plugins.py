from typing import Optional

from cleo import Command
from pkg_resources import EntryPoint

from aiogram_cli.loader import ExtensionsLoader


class PluginsListCommand(Command):
    name = "plugins"
    description = "Get installed plugins list"
    help = description
    hidden = True

    def handle(self) -> Optional[int]:
        loader = ExtensionsLoader()
        for index, entry_point in enumerate(loader.iter_entry_points(), start=1):
            line = f"{index:>3}. {self.format_entry_point(entry_point)}"
            self.line(line)

        return 0

    @classmethod
    def format_entry_point(cls, entry_point: EntryPoint) -> str:
        line = f"<info>{entry_point.name}</info> from <info>{entry_point.module_name}</info>"
        if entry_point.attrs:
            line += " by <info>" + ".".join(entry_point.attrs) + "</info>"
        if entry_point.extras:
            line += (
                " with extras [" + ", ".join(f"<info>{s}</info>" for s in entry_point.extras) + "]"
            )
        return line
