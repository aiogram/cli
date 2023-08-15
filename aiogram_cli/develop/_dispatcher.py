import inspect
from typing import Any

from aiogram import Bot, Dispatcher

from aiogram_cli.develop._resolver import logger, resolve_import


async def do_skip_updates(bot: Bot):
    logger.warning("Skipping updates")
    await bot.delete_webhook(drop_pending_updates=True)


def resolve_dispatcher(*, target: str) -> Dispatcher:
    return resolve_import(target=target, possible_names={"dp", "dispatcher"})


async def prepare_dispatcher(*, dispatcher: Any, skip_updates: bool) -> Dispatcher:
    if callable(dispatcher):
        dispatcher = dispatcher()

    if inspect.isawaitable(dispatcher):
        dispatcher = await dispatcher

    if not isinstance(dispatcher, Dispatcher):
        msg = f"Dispatcher must be instance of aiogram.Dispatcher, got: {type(dispatcher)}"
        raise ValueError(msg)

    if skip_updates:
        dispatcher.startup.register(do_skip_updates)

    return dispatcher


def simplified_prepare_dispatcher(*, dispatcher: Any, skip_updates: bool) -> Dispatcher:
    if callable(dispatcher):
        dispatcher = dispatcher()

    if not isinstance(dispatcher, Dispatcher):
        msg = f"Dispatcher must be instance of aiogram.Dispatcher, got: {type(dispatcher)}"
        raise ValueError(msg)

    if skip_updates:
        dispatcher.startup.register(do_skip_updates)

    return dispatcher
