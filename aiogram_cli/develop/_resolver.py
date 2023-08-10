import importlib
import logging

from aiogram import Bot, Dispatcher

logger = logging.getLogger(__name__)


class LoadError(Exception):
    pass


def resolve_dispatcher(*, target: str, skip_updates: bool) -> Dispatcher:
    module_name, _, target_name = target.partition(":")

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        msg = f"Can't import module: {module_name!r}"
        raise LoadError(msg) from None

    if not target_name:
        for name in ["dp", "dispatcher"]:
            if hasattr(module, name):
                target_name = name
                break
        else:
            msg = f"Can't find dispatcher in module: {module_name!r}"
            raise LoadError(msg)

    dispatcher = getattr(module, target_name, None)
    if not dispatcher:
        msg = f"Can't find dispatcher in module: {module_name!r} by name: {target_name!r}"
        raise LoadError(msg)

    if callable(dispatcher):
        dispatcher = dispatcher()

    if not isinstance(dispatcher, Dispatcher):
        msg = f"Dispatcher must be instance of aiogram.Dispatcher, got: {type(dispatcher)}"
        raise LoadError(msg)

    if skip_updates:
        dispatcher.startup.register(_skip_updates)

    return dispatcher


async def _skip_updates(bot: Bot):
    logger.warning("Skipping updates")
    await bot.delete_webhook(drop_pending_updates=True)
