import asyncio
import sys
from logging import basicConfig
from typing import Any

import aiogram
import click
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from aiogram_cli.develop._bot import create_bot
from aiogram_cli.develop._dispatcher import prepare_dispatcher, resolve_dispatcher
from aiogram_cli.develop._resolver import LoadError


def start_polling(
    *,
    target: str,
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
    click.echo(f"Running bot on aiogram v{aiogram.__version__} in polling mode")

    click.echo("Loading application...")
    try:
        dispatcher = resolve_dispatcher(target=target)
    except LoadError as e:
        click.echo(str(e), err=True)
        sys.exit(2)

    bot = create_bot(token=token, default=defaults, api_address=api_address)

    asyncio.run(_polling(bot=bot, dispatcher=dispatcher, skip_updates=skip_updates))
    return 0


async def _polling(
    *,
    dispatcher: Any,
    bot: Bot,
    skip_updates: bool = False,
):
    try:
        dispatcher = await prepare_dispatcher(dispatcher=dispatcher, skip_updates=skip_updates)
        async with bot:
            await dispatcher.start_polling(bot, close_bot_session=False)
    except Exception as e:
        click.echo(f"Application startup failed - {type(e).__name__}: {e}", err=True)
        raise

