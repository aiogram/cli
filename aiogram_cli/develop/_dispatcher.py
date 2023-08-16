import inspect
from typing import Any

import click
from aiogram import Bot, Dispatcher, Router

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

    _add_status_watcher(dispatcher)

    return dispatcher


def simplified_prepare_dispatcher(*, dispatcher: Any, skip_updates: bool) -> Dispatcher:
    if callable(dispatcher):
        dispatcher = dispatcher()

    if not isinstance(dispatcher, Dispatcher):
        msg = f"Dispatcher must be instance of aiogram.Dispatcher, got: {type(dispatcher)}"
        raise ValueError(msg)

    if skip_updates:
        dispatcher.startup.register(do_skip_updates)

    _add_status_watcher(dispatcher)

    return dispatcher


def _add_status_watcher(dispatcher: Dispatcher):
    last_router = Router(name="_aiogram_cli_status")
    dispatcher.include_router(last_router)

    last_router.startup.register(startup_completed_callback)
    last_router.shutdown.register(shutdown_completed_callback)


async def startup_completed_callback():
    click.echo("Application started")


async def shutdown_completed_callback():
    click.echo("Application stopped")
