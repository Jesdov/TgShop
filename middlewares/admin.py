from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, Update
from typing import Callable, Dict, Any, Awaitable

from bot import bot


class admin_check(BaseMiddleware):
    def __init__(self, admin_list: list):
        self.admin_list = admin_list

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if (event.from_user.id in self.admin_list):
            return await handler(event, data)