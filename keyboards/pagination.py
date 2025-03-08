from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from database import requests as rq

class Pagination(CallbackData, prefix="pag"):
    page: int

class ProductData(CallbackData, prefix="prod"):
    purschase_id: int

class Buy_category(CallbackData, prefix = "buy_cat"):
    category_id: int

class Buy_item(CallbackData, prefix = "buy_item"):
    category_id: int
    item_id: int

class Buy_item_one_or_many(CallbackData, prefix = "buy_item"):
    category_id: int
    item_id: int
    count: int

class PaginationApeals(CallbackData, prefix="apeal"):
    page: int

class ApealsData(CallbackData, prefix="apeal_data"):
    id: int

async def get_paginated_kb(user_id: str, page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()  

    purschases = await rq.get_purschases(user_id)
    start_offset = page * 5
    end_offset = start_offset + 5

    for purschase in purschases[start_offset:end_offset]:  
        builder.row(InlineKeyboardButton(text = f'{purschase.name_of_purschase} | {purschase.sum_of_purschase}₽', callback_data=ProductData(purschase_id=purschase.id).pack()))

    buttons_row = []
    if page > 0:  
        buttons_row.append(  
            InlineKeyboardButton(  
                text="⬅️",  
                callback_data=Pagination(page=page - 1).pack(),  
            )  
        )  
    if end_offset < len(purschases):  
        buttons_row.append(  
            InlineKeyboardButton(  
                text="➡️",  
                callback_data=Pagination(page=page + 1).pack(),  
            )  
        )
    builder.row(*buttons_row)
    
    return builder.as_markup()

async def back_to_history():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text = f'⬅️ Назад', callback_data=Pagination(page=0).pack()))
    return keyboard.adjust(1).as_markup()

async def buy_kb_categories() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()  

    categories = await rq.get_categories()
    for category in categories: 
        keyboard.add(InlineKeyboardButton(text = f'{category.name}', callback_data=Buy_category(category_id = category.id).pack()))
    
    return keyboard.adjust(2).as_markup()

async def buy_kb_items(category_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()  

    items = await rq.get_items(category_id)
    for item in items:
        if (item.amount > 0):
            keyboard.add(InlineKeyboardButton(text = f'{item.name} | {item.price}₽', callback_data = Buy_item(category_id=category_id, item_id=item.id).pack()))
    keyboard.add(InlineKeyboardButton(text = f'⬅️ Назад', callback_data="back"))
    
    return keyboard.adjust(2).as_markup()

async def buy_kb_one__or_many(category_id: int, item_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text = "Купить 1 шт", callback_data = f"buy_one_item_{item_id}"))
    keyboard.add(InlineKeyboardButton(text = "Купить несколько", callback_data = f"buy_more_item_{item_id}"))
    keyboard.add(InlineKeyboardButton(text = f'⬅️ Назад', callback_data=Buy_category(category_id = category_id).pack()))
    return keyboard.adjust(2).as_markup()


async def get_apeals_kb(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()  

    apeals = await rq.get_apeals()
    start_offset = page * 7
    end_offset = start_offset + 7

    for apeal in apeals[start_offset:end_offset]:  
        builder.row(InlineKeyboardButton(text = f'{apeal.tg_id} | {apeal.appeal[:25]}', callback_data=ApealsData(id = apeal.id).pack()))

    buttons_row = []
    if page > 0:  
        buttons_row.append(  
            InlineKeyboardButton(  
                text="⬅️",  
                callback_data=PaginationApeals(page=page - 1).pack(),  
            )  
        )  
    if end_offset < len(apeals):  
        buttons_row.append(  
            InlineKeyboardButton(  
                text="➡️",  
                callback_data=PaginationApeals(page=page + 1).pack(),  
            )  
        )
    builder.row(*buttons_row)
    
    return builder.as_markup()


async def appeals_handler(appeal_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text = f'💬 Ответить', callback_data = f'appeal_answer_{appeal_id}'))
    keyboard.add(InlineKeyboardButton(text = f'❌ Удалить', callback_data = f'appeal_delete_{appeal_id}'))
    keyboard.add(InlineKeyboardButton(text = f'⬅️ Назад', callback_data = f'appeals_back'))
    return keyboard.adjust(1).as_markup()