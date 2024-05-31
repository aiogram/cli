import logging
import ssl
import sys
from logging import basicConfig
from pathlib import Path
from typing import Any

import aiogram
import click
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import Application, run_app

from aiogram_cli.develop._bot import create_bot
from aiogram_cli.develop._dispatcher import prepare_dispatcher, resolve_dispatcher
from aiogram_cli.develop._resolver import LoadError

logger = logging.getLogger(__name__)


def start_webhook(
    *,
    target: str,
    host: str,
    port: int,
    path: str,
    webhook_address: str | None,
    webhook_secret: str | None,
    ssl_certificate: Path | None,
    ssl_private_key: Path | None,
    token: str,
    defaults: DefaultBotProperties,
    skip_updates: bool,
    api_address: str,
    log_level: str,
    log_format: str,
) -> int:
    if log_level:
        basicConfig(level=log_level, format=log_format)

    click.echo("=" * 80)
    click.echo(f"Running bot on aiogram v{aiogram.__version__} in webhook mode")

    click.echo("Loading application...")
    try:
        dispatcher = resolve_dispatcher(target=target)
    except LoadError as e:
        click.echo(str(e), err=True)
        sys.exit(2)

    bot = create_bot(token=token, default=defaults, api_address=api_address)
    click.echo("Start webhook")

    if ssl_certificate and ssl_private_key:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(ssl_certificate, ssl_private_key)
    else:
        context = None

    logger.info("Starting web application on %s:%s", host, port)
    run_app(
        _create_app(
            bot=bot,
            dispatcher=dispatcher,
            path=path,
            webhook_address=webhook_address,
            webhook_secret=webhook_secret,
            ssl_certificate=ssl_certificate,
            skip_updates=skip_updates,
        ),
        host=host,
        port=port,
        ssl_context=context,
        print=logging.getLogger("aiohttp.server").info,
    )
    return 0


async def _create_app(
    *,
    bot: Bot,
    dispatcher: Any,
    path: str,
    webhook_address: str | None,
    webhook_secret: str | None,
    ssl_certificate: Path | None,
    skip_updates: bool,
) -> Application:
    app = Application()
    try:
        dispatcher = await prepare_dispatcher(dispatcher=dispatcher, skip_updates=skip_updates)
        setup_application(app, dispatcher, bot=bot)
    except Exception as e:
        click.echo(f"Application startup failed - {type(e).__name__}: {e}", err=True)
        raise

    SimpleRequestHandler(dispatcher=dispatcher, bot=bot, secret_token=webhook_secret).register(app, path=path)

    async def _setup_webhook():
        logger.info("Setting up webhook to %s", webhook_address)
        if ssl_certificate:
            certificate = FSInputFile(ssl_certificate)
        else:
            certificate = None
        await bot.set_webhook(url=webhook_address, secret_token=webhook_secret, certificate=certificate)

    if webhook_address:
        dispatcher.startup.register(_setup_webhook)

    return app
