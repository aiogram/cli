import click
from pkg_resources import DistInfoDistribution, EntryPoint, iter_entry_points


@click.command("plugins")
def command_plugins():
    """Get a list of available plugins"""
    entrypoint: EntryPoint
    for index, entrypoint in enumerate(iter_entry_points("aiogram_cli.plugins"), start=1):
        dist: DistInfoDistribution = entrypoint.dist
        plugin = entrypoint.load()
        description = plugin.__doc__.split("\n")[0] if plugin.__doc__ else ""

        click.echo(f"{index:3}.", nl=False)
        click.secho(f" {entrypoint.name}", fg="green", nl=False)
        click.echo(f" (from {dist.project_name} v{dist.version})", nl=False)
        if description:
            click.echo(f": {description}")
        else:
            click.echo()
