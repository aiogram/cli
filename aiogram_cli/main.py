import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points

from aiogram_cli import __version__


@with_plugins(iter_entry_points("aiogram_cli.plugins"))
@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(version=__version__, prog_name="aiogram-cli", message="%(version)s")
def cli():
    pass
