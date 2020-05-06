from typing import Optional

import aiogram
from cleo import Command

import aiogram_cli


class AboutCommand(Command):
    name = "about"
    description = "Get application info"
    help = description

    def handle(self) -> Optional[int]:
        self.line(f"aiogram-cli: <comment>v{aiogram_cli.__version__}</comment>")
        self.line(f"aiogram: <comment>v{aiogram.__version__}</comment>")

        return 0
