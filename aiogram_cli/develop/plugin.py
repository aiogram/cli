from logging import getLevelNamesMapping
from os import getenv
from pathlib import Path

import click
from aiogram.enums import ParseMode
from click import Choice
from watchfiles import run_process
from watchfiles.main import FileChange

from aiogram_cli.develop._polling import start_polling
from aiogram_cli.develop._webhook import start_webhook


@click.group("run")
def develop_runner():
    """Run bot in development mode"""


@develop_runner.command("polling")
@click.argument(
    "dispatcher",
    required=True,
)
@click.option(
    "--token",
    "-t",
    help="Bot token",
    required=True,
    default=getenv("TELEGRAM_TOKEN"),
)
@click.option(
    "--parse-mode",
    type=Choice(ParseMode),
    help="Default parse mode",
    default=ParseMode.HTML,
)
@click.option(
    "--disable-web-page-preview",
    is_flag=True,
    help="Disable web page preview by default",
)
@click.option(
    "--protect-content",
    is_flag=True,
    help="Protect content from telegram clients by default",
)
@click.option(
    "--skip-updates",
    help="Skip updates",
    is_flag=True,
)
@click.option(
    "--log-level",
    "-l",
    type=Choice(list(getLevelNamesMapping().keys())),
    help="Logging level",
)
@click.option(
    "--log-format",
    "-f",
    help="Logging format",
    default="%(asctime)s %(levelname)10s %(name)s: %(message)s",
)
@click.option(
    "--reload",
    "-r",
    help="Reload modules",
    is_flag=True,
)
@click.option(
    "--reload-path",
    "-p",
    help="Reload modules",
    multiple=True,
)
def command_polling(
    *,
    dispatcher: str,
    token: str,
    parse_mode: ParseMode,
    disable_web_page_preview: bool,
    protect_content: bool,
    skip_updates: bool,
    reload: bool,
    log_level: str,
    log_format: str,
    reload_path: tuple[str],
):
    """
    Run bot in development mode with polling updates
    """
    if not reload_path:
        reload_path = (str(Path().resolve()),)

    kwargs = {
        "target": dispatcher,
        "token": token,
        "parse_mode": parse_mode,
        "skip_updates": skip_updates,
        "disable_web_page_preview": disable_web_page_preview,
        "protect_content": protect_content,
        "log_level": log_level,
        "log_format": log_format,
    }
    if reload:
        run_process(
            *reload_path,
            target=start_polling,
            kwargs=kwargs,
            callback=_changes_detected,
        )
    else:
        return start_polling(**kwargs)


@develop_runner.command("webhook")
@click.argument(
    "dispatcher",
    required=True,
)
@click.option(
    "--host",
    "-h",
    help="Webhook host",
    default="localhost",
)
@click.option(
    "--port",
    "-p",
    help="Webhook port",
    default=8080,
)
@click.option(
    "--path",
    help="Webhook path",
    default="/webhook",
)
@click.option(
    "--ssl-certificate",
    help="SSL certificate path",
)
@click.option(
    "--ssl-private-key",
    help="SSL private key path",
)
@click.option(
    "--address",
    help="Webhook address to be passed into setWebhook method",
)
@click.option(
    "--secret",
    help="Webhook secret to be passed into setWebhook method",
)
@click.option(
    "--token",
    "-t",
    help="Bot token",
    required=True,
    default=getenv("TELEGRAM_TOKEN"),
)
@click.option(
    "--parse-mode",
    type=Choice(ParseMode),
    help="Default parse mode",
    default=ParseMode.HTML,
)
@click.option(
    "--disable-web-page-preview",
    is_flag=True,
    help="Disable web page preview by default",
)
@click.option(
    "--protect-content",
    is_flag=True,
    help="Protect content from telegram clients by default",
)
@click.option(
    "--skip-updates",
    help="Skip updates",
    is_flag=True,
)
@click.option(
    "--log-level",
    "-l",
    type=Choice(list(getLevelNamesMapping().keys())),
    help="Logging level",
)
@click.option(
    "--log-format",
    "-f",
    help="Logging format",
    default="%(asctime)s %(levelname)10s %(name)s: %(message)s",
)
@click.option(
    "--reload",
    "-r",
    help="Reload modules",
    is_flag=True,
)
@click.option(
    "--reload-path",
    "-p",
    help="Reload modules",
    multiple=True,
)
def command_webhook(
    *,
    dispatcher: str,
    host: str,
    port: int,
    path: str,
    ssl_certificate: str,
    ssl_private_key: str,
    address: str,
    secret: str,
    token: str,
    parse_mode: ParseMode,
    disable_web_page_preview: bool,
    protect_content: bool,
    skip_updates: bool,
    reload: bool,
    log_level: str,
    log_format: str,
    reload_path: tuple[str],
):
    """
    Run bot in development mode with webhook updates
    """
    if not reload_path:
        reload_path = (str(Path().resolve()),)

    kwargs = {
        "target": dispatcher,
        "host": host,
        "port": port,
        "path": path,
        # "ssl_certificate": ssl_certificate,
        # "ssl_private_key": ssl_private_key,
        "webhook_address": address,
        "webhook_secret": secret,
        "token": token,
        "parse_mode": parse_mode,
        "skip_updates": skip_updates,
        "disable_web_page_preview": disable_web_page_preview,
        "protect_content": protect_content,
        "log_level": log_level,
        "log_format": log_format,
    }
    if reload:
        run_process(
            *reload_path,
            target=start_webhook,
            kwargs=kwargs,
            callback=_changes_detected,
        )
    else:
        return start_webhook(**kwargs)


def _changes_detected(changes: set[FileChange]):
    files = {path for change, path in changes}
    click.echo(f"Changes detected: {files}")
