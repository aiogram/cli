from typing import Any

from cleo import Application

from aiogram_cli import __version__
from aiogram_cli.loader import ExtensionsLoader


def get_application() -> Application:
    app = Application("aiogram-cli", __version__)

    loader = ExtensionsLoader()
    loader.setup(app=app)

    return app


def main() -> Any:
    app = get_application()
    return app.run()
