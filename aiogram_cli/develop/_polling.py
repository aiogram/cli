import asyncio
import sys
from logging import basicConfig
from typing import Any

import aiogram
import click
from aiogram import Bot
from aiogram.enums import ParseMode

from aiogram_cli.develop._dispatcher import prepare_dispatcher, resolve_dispatcher
from aiogram_cli.develop._resolver import LoadError


def start_polling(
    *,
    target: str,
    token: str,
    parse_mode: ParseMode,
    disable_web_page_preview: bool,
    protect_content: bool,
    skip_updates: bool,
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

    # TODO: Add possibility to specify bot instance
    bot = Bot(
        token=token,
        parse_mode=parse_mode,
        disable_web_page_preview=disable_web_page_preview,
        protect_content=protect_content,
    )

    asyncio.run(_polling(bot=bot, dispatcher=dispatcher, skip_updates=skip_updates))
    return 0


async def _polling(
    *,
    dispatcher: Any,
    bot: Bot,
    skip_updates: bool = False,
):
    dispatcher = await prepare_dispatcher(dispatcher=dispatcher, skip_updates=skip_updates)
    async with bot.context() as bot:
        await dispatcher.start_polling(bot, close_bot_session=False)
