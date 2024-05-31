from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from aiogram_cli.develop._server_address import ensure_telegram_api_server


def create_bot(
    *,
    token: str,
    default: DefaultBotProperties | None,
    api_address: str,
) -> Bot:
    api = ensure_telegram_api_server(api_address)
    session = AiohttpSession(
        api=api,
        # proxy=None,  # TODO: add proxy support
    )

    return Bot(
        token=token,
        default=default,
        session=session,
    )
