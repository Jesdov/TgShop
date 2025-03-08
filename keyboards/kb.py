from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import requests as rq

main_admin = ReplyKeyboardMarkup(
    keyboard=
    [
        [KeyboardButton(text = "🙍‍♂️\tМой профиль"), KeyboardButton(text = "🛒\tТовары")],

        [KeyboardButton(text = "💰\tКупить"), KeyboardButton(text = "📩\tТех. Поддержка")],
        
        [KeyboardButton(text = "⚒️\tStaff\t⚒️")]
    ],
    resize_keyboard=True
)

main_user = ReplyKeyboardMarkup(
    keyboard=
    [
        [KeyboardButton(text = "🙍‍♂️\tМой профиль"), KeyboardButton(text = "🛒\tТовары")],

        [KeyboardButton(text = "💰\tКупить"), KeyboardButton(text = "📩\tТех. Поддержка")],
        
    ],
    resize_keyboard=True
)

profile_user = ReplyKeyboardMarkup(
    keyboard=
    [
        [KeyboardButton(text = "💰\tПополнить"), KeyboardButton(text = "🛒\tИстория покупок")],

        [KeyboardButton(text = "🔙\tНа главную")],
        
    ],
    resize_keyboard=True
)

admin_panel = ReplyKeyboardMarkup(
        keyboard=
    [
        [KeyboardButton(text = "🛒\tДобавить категорию"), KeyboardButton(text = "🛍️\tДобавить товар"), KeyboardButton(text = "📦\tДобавить данные товара")],

        [KeyboardButton(text = "🗑️\tУдалить категорию"), KeyboardButton(text = "⛔\tУдалить товар"), KeyboardButton(text = "❌\tУдалить данные товара")],
        [KeyboardButton(text = "✉️\tРассылка"), KeyboardButton(text = "🛑\t Забанить пользователя"), KeyboardButton(text = "📝\tРазбанить пользователя")],
        [KeyboardButton(text = "💬\tОбращения"), KeyboardButton(text = "🔙\tНа главную")]
    ],
    resize_keyboard=True
)

async def items_add_categories():
    keyboard = InlineKeyboardBuilder()
    all_categories = await rq.get_categories()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f"add_item_{category.id}"))
    return keyboard.adjust(2).as_markup()



async def data_add_categories():
    keyboard = InlineKeyboardBuilder()
    all_categories = await rq.get_categories()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f"add_data_category_{category.id}"))
    return keyboard.adjust(2).as_markup()

async def data_items_categories(id: int):
    keyboard = InlineKeyboardBuilder()
    all_items = await rq.get_items(id)
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text = f'{item.name} - {item.price}₽', callback_data = f"add_data_item_{item.id}"))
    return keyboard.adjust(2).as_markup()


    
async def delete_categories():
    keyboard = InlineKeyboardBuilder()
    all_categories = await rq.get_categories()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f"delete_category_{category.id}"))
    return keyboard.adjust(2).as_markup()




async def delete_items_categories():
    keyboard = InlineKeyboardBuilder()
    all_categories = await rq.get_categories()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f"delete_item_category_{category.id}"))
    return keyboard.adjust(2).as_markup()

async def delete_items(id: int):
    keyboard = InlineKeyboardBuilder()
    all_items = await rq.get_items(id)
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text = f'{item.name} - {item.price}₽', callback_data = f"delete_item_{item.id}"))
    return keyboard.adjust(2).as_markup()





async def delete_data_categories():
    keyboard = InlineKeyboardBuilder()
    all_categories = await rq.get_categories()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f"delete_data_category_{category.id}"))
    return keyboard.adjust(2).as_markup()

async def delete_data_items(id : int):
    keyboard = InlineKeyboardBuilder()
    all_items = await rq.get_items(id)
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text = f'{item.name} - {item.price}₽', callback_data = f"delete_data_item_{item.id}"))
    return keyboard.adjust(2).as_markup()

async def accept_buy_1(item_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text = "👌 Подтверждаю", callback_data = f"accept_1_item_{item_id}"))
    return keyboard.adjust(2).as_markup()

async def deposit():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text = "💵 Пополнить баланс", callback_data = f"deposit"))
    return keyboard.adjust(2).as_markup()

async def accept_buy_many(item_id: int, item_count: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text = "👌 Подтверждаю", callback_data = f"accept_{item_count}_item_{item_id}"))
    return keyboard.adjust(2).as_markup()


async def history_of_purschase(user_id: int):
    keyboard = InlineKeyboardBuilder()
    purschases = await rq.get_purschases(user_id)
    for purschase in purschases:
        keyboard.add(InlineKeyboardButton(text = f'{purschase.name_of_purschase} | {purschase.sum_of_purschase}₽', callback_data = f"history_{purschase.id}"))
    return keyboard.adjust(1).as_markup()

async def subscribe_check():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text = f'↗️\tПодписаться', url = "t.me/+KrHkXB4lkiQ5YzFi"))
    keyboard.add(InlineKeyboardButton(text = f'❓️\tПроверить подписку', callback_data = f'check_subcr'))
    return keyboard.adjust(1).as_markup()









