from aiogram.client.telegram import PRODUCTION as _PRODUCTION
from aiogram.client.telegram import TEST as _TEST
from aiogram.client.telegram import TelegramAPIServer

MAIN = _PRODUCTION
TEST = _TEST
BETA = TelegramAPIServer(
    base="https://api.telegram.org/beta/bot{token}/{method}",
    file="https://api.telegram.org/beta/file/bot{token}/{path}",
)


def ensure_telegram_api_server(address: str) -> TelegramAPIServer:
    if address == "main":
        return MAIN
    if address == "test":
        return TEST
    if address == "beta":
        return BETA

    if not address.startswith("http"):
        msg = f"Invalid server address: {address!r}"
        raise ValueError(msg)
    return TelegramAPIServer.from_base(address)
