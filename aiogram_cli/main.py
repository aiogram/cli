from collections import defaultdict
from importlib.metadata import EntryPoint

import aiogram
import click
from click_plugins import with_plugins

from aiogram_cli import __version__
from aiogram_cli.resolver import iter_entry_points


@with_plugins(iter_entry_points("aiogram_cli.plugins"))
@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(version=__version__, prog_name="aiogram-cli", message="%(version)s")
def cli():
    pass


@cli.command("version")
def command_version():
    """Get an application version"""
    click.echo(f"aiogram-cli: v{__version__}")
    click.echo(f"aiogram: v{aiogram.__version__}")


@cli.command("plugins")
def command_plugins():
    """Get a list of available plugins"""
    entrypoint: EntryPoint
    broken_libs = defaultdict(set)
    for index, entrypoint in enumerate(iter_entry_points("aiogram_cli.plugins"), start=1):
        click.echo(f"{index:3}.", nl=False)

        dist = entrypoint.dist
        try:
            plugin = entrypoint.load()
        except Exception as e:
            broken_libs[dist.name].add(entrypoint.name)
            click.secho(f" {entrypoint.name}", fg="red", err=True, nl=False)
            click.echo(f" (by {dist.name} v{dist.version})", err=True, nl=False)
            click.echo(f" is unusable in due to {type(e).__name__}: {e}")
            continue

        description = plugin.__doc__.split("\n")[0] if plugin.__doc__ else ""

        click.secho(f" {entrypoint.name}", fg="green", nl=False)
        click.echo(f" (by {dist.name} v{dist.version})", nl=False)
        if description:
            click.echo(f": {description}")
        else:
            click.echo()

    if broken_libs:
        click.echo()
        click.secho("Broken libraries:", fg="red", err=True)
        for lib, plugins in broken_libs.items():
            click.echo(f"  {lib} ({', '.join(plugins)})")
