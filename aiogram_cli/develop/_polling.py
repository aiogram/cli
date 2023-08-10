import asyncio
import sys
from logging import basicConfig

import aiogram
import click
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from aiogram_cli.develop._resolver import LoadError, resolve_dispatcher


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
        dispatcher = resolve_dispatcher(target=target, skip_updates=skip_updates)
    except LoadError as e:
        click.echo(str(e), err=True)
        sys.exit(2)

    bot = Bot(
        token=token,
        parse_mode=parse_mode,
        disable_web_page_preview=disable_web_page_preview,
        protect_content=protect_content,
    )
    click.echo("Start polling")
    asyncio.run(_polling(bot=bot, dispatcher=dispatcher))
    return 0


async def _polling(
    *,
    dispatcher: Dispatcher,
    bot: Bot,
):
    async with bot.context() as bot:
        await dispatcher.start_polling(bot, close_bot_session=False)
