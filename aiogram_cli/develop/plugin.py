import functools
import sys
from contextlib import suppress
from os import getenv
from pathlib import Path

import click
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from click import Choice, style
from watchfiles import run_process
from watchfiles.main import FileChange

from aiogram_cli.develop._polling import start_polling
from aiogram_cli.develop._webhook import start_webhook
from aiogram_cli.wraps import async_command

LOGGING_LEVELS = [
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARN",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
]


@click.group("run")
def develop_runner():
    """Run bot in development mode"""
    sys.path.append(str(Path().resolve()))


def defaults_options(func):
    @click.option("--parse-mode", type=Choice(ParseMode), help="Default parse mode", default=ParseMode.HTML.value)
    @click.option("--protect-content", is_flag=True, help="Protect content from telegram clients by default")
    @click.option("--disable-notification", is_flag=True, help="Disable notification by default")
    @click.option("--allow-sending-without-reply", is_flag=True, help="Allow sending messages without reply by default")
    @click.option("--disable-web-page-preview", is_flag=True, help="[DEPRECATED] Disable web page preview by default")
    @click.option("--link-preview-is-disabled", is_flag=True, help="Disable web page preview by default")
    @click.option("--link-preview-prefer-small-media", is_flag=True, help="Prefer small media for link preview")
    @click.option("--link-preview-prefer-large-media", is_flag=True, help="Prefer large media for link preview")
    @click.option("--link-preview-show-above-text", is_flag=True, help="Show link preview above text")
    @functools.wraps(func)
    def _wrapper(
            *args,
            parse_mode: ParseMode | None,
            protect_content: bool | None,
            disable_notification: bool | None,
            allow_sending_without_reply: bool | None,
            disable_web_page_preview: bool | None,
            link_preview_is_disabled: bool | None,
            link_preview_prefer_small_media: bool | None,
            link_preview_prefer_large_media: bool | None,
            link_preview_show_above_text: bool | None,
            **kwargs,
    ):
        if disable_web_page_preview:
            click.secho(
                "Option --disable-web-page-preview is deprecated, use --link-preview-is-disabled instead",
                fg="yellow",
            )
        kwargs["defaults"] = DefaultBotProperties(
            parse_mode=parse_mode or None,
            protect_content=protect_content or None,
            disable_notification=disable_notification or None,
            allow_sending_without_reply=allow_sending_without_reply or None,
            link_preview_is_disabled=link_preview_is_disabled or disable_web_page_preview or None,
            link_preview_prefer_small_media=link_preview_prefer_small_media or None,
            link_preview_prefer_large_media=link_preview_prefer_large_media or None,
            link_preview_show_above_text=link_preview_show_above_text or None,
        )
        return func(*args, **kwargs)

    return _wrapper


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
    envvar="TELEGRAM_TOKEN",
)
@click.option(
    "--skip-updates",
    help="Skip updates",
    is_flag=True,
)
@click.option(
    "--log-level",
    "-l",
    type=Choice(LOGGING_LEVELS, case_sensitive=False),
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
@defaults_options
def command_polling(
        *,
        dispatcher: str,
        token: str,
        defaults: DefaultBotProperties,
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
        "skip_updates": skip_updates,
        "log_level": log_level,
        "log_format": log_format,
        "defaults": defaults,
    }
    with suppress(KeyboardInterrupt):
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
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--ssl-private-key",
    help="SSL private key path",
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--address",
    help="Webhook address to be passed into setWebhook method",
)
@click.option(
    "--secret",
    help="Webhook secret to be passed into setWebhook method",
    envvar="TELEGRAM_WEBHOOK_SECRET",
)
@click.option(
    "--token",
    "-t",
    help="Bot token",
    required=True,
    envvar="TELEGRAM_TOKEN",
)
@click.option(
    "--skip-updates",
    help="Skip updates",
    is_flag=True,
)
@click.option(
    "--log-level",
    "-l",
    type=Choice(LOGGING_LEVELS, case_sensitive=False),
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
@defaults_options
def command_webhook(
        *,
        dispatcher: str,
        host: str,
        port: int,
        path: str,
        ssl_certificate: Path | None,
        ssl_private_key: Path | None,
        address: str | None,
        secret: str | None,
        token: str,
        defaults: DefaultBotProperties,
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
        "ssl_certificate": ssl_certificate,
        "ssl_private_key": ssl_private_key,
        "webhook_address": address,
        "webhook_secret": secret,
        "token": token,
        "skip_updates": skip_updates,
        "defaults": defaults,
        "log_level": log_level,
        "log_format": log_format,
    }
    with suppress(KeyboardInterrupt):
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


@develop_runner.command("info")
@click.option(
    "--token",
    "-t",
    help="Bot token",
    required=True,
    default=getenv("TELEGRAM_TOKEN"),
)
@async_command
async def command_info(token: str):
    async with Bot(token=token).context() as bot:
        me = await bot.get_me()
        webhook_info = await bot.get_webhook_info()

    click.echo(style("Bot info:", fg="green", bold=True))
    click.echo("  " + style("ID: ", bold=True, fg="green") + str(me.id))
    click.echo("  " + style("Username: ", bold=True, fg="green") + f"@{me.username} (https://t.me/{me.username})")
    click.echo("  " + style("Name: ", bold=True, fg="green") + me.full_name)
    if me.is_premium:
        click.echo("  " + style("Premium: ", bold=True, fg="green") + "Yes")
    if webhook_info.url:
        click.echo(
            style("Webhook info:", fg="green", bold=True),
        )
        click.echo("  " + style("URL: ", bold=True, fg="green") + webhook_info.url)
    if webhook_info.allowed_updates:
        click.echo("  " + style("Allowed updates: ", bold=True, fg="green") + ", ".join(webhook_info.allowed_updates))
    if webhook_info.ip_address:
        click.echo("  " + style("IP address: ", bold=True, fg="green") + webhook_info.ip_address)
    if webhook_info.has_custom_certificate:
        click.echo("  " + style("Has custom certificate: ", bold=True, fg="green") + "Yes")
    if webhook_info.pending_update_count:
        click.echo("  " + style("Pending updates: ", bold=True, fg="green") + str(webhook_info.pending_update_count))
    if webhook_info.last_error_date:
        click.echo("  " + style("Last error date: ", bold=True, fg="green") + str(webhook_info.last_error_date))
    if webhook_info.last_error_message:
        click.echo("  " + style("Last error message: ", bold=True, fg="green") + webhook_info.last_error_message)
    if webhook_info.max_connections:
        click.echo("  " + style("Max connections: ", bold=True, fg="green") + str(webhook_info.max_connections))
    if webhook_info.last_synchronization_error_date:
        click.echo(
            "  "
            + style("Last synchronization error date: ", bold=True, fg="green")
            + str(webhook_info.last_synchronization_error_date)
        )
