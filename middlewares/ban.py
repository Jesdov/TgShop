from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, Update
from typing import Callable, Dict, Any, Awaitable

from bot import bot

from keyboards import kb

class ban_check(BaseMiddleware):
    def __init__(self, ban_list: list):
        self.ban_list = ban_list

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and "/start" in event.text:
            return await handler(event, data)
        
        sub = await bot.get_chat_member(chat_id = -1002263423567, user_id = event.from_user.id)
        if (event.from_user.id not in self.ban_list):
            if sub.status == "left":
                await bot.send_message(chat_id = event.from_user.id, text = "Вы не подписаны на канал", reply_markup= await kb.subscribe_check())
            else:
                return await handler(event, data)