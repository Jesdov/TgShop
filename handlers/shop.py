from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from asyncio import sleep
from database import requests as rq
from config import admin_list

from bot import bot

import keyboards.kb as kb
import keyboards.pagination as pag

class many_items(StatesGroup):
    item = State()

class appeals(StatesGroup):
    appeal = State()

router = Router()
@router.message(Command("start"))
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    get_user = await rq.get_user(message.from_user.id)
    arguments = []
    try:
        arguments = command.args.split("_")
    except:
        pass
    if not arguments:
        if not get_user:
            await rq.set_user(message.from_user.id)
        if message.from_user.id in admin_list:
            kbrd = kb.main_admin
        else:
            kbrd = kb.main_user
        await message.answer('''🎉 Добро пожаловать в наш телеграм-бот по продажам товаров! ✨ Мы рады видеть тебя здесь! 
                            
    🔎 Ищешь что-то особенное? У нас есть всё: от модной одежды до гаджетов и много другого!

    💬 Если у тебя возникнут вопросы или нужна помощь, просто напиши — мы всегда на связи!

    Начни шопинг уже сейчас и найдите свои идеальные покупки!

    Приятного времяпрепровождения! 🎈''', reply_markup=kbrd)
        
    elif len(arguments) == 2 and arguments[0] == "c":
        if not get_user:
            await rq.set_user(message.from_user.id)
        await message.answer(
            text = "Выберите название товара", 
            reply_markup = await pag.buy_kb_items(int(arguments[1]))
        )

    elif len(arguments) == 3 and arguments[0] == "c":
        if not get_user:
            await rq.set_user(message.from_user.id)
        text_message = ''
        category_id = int(arguments[1])
        item_id = int(arguments[2])
        item = await rq.buy_info_item(item_id)
        user = await rq.get_user(message.from_user.id)
        text_message += f'──── Покупка ──── \n\n🛒\tТовар:\t{item.name}\n💰\tЦена:\t{item.price}₽\n📑\tКол-во:\t{item.amount}\n📝\tОписание: {item.description}\n\n💲\tВаш баланс:\t{user.balance}₽'
        await message.answer(
            text_message, 
            reply_markup = await pag.buy_kb_one__or_many(category_id, item_id)
        )

    elif len(arguments) == 2 and arguments[0] == "r" and not get_user:
        who_invited_id = int(arguments[1])
        await rq.set_user(message.from_user.id, who_invited_id)
        if message.from_user.id in admin_list:
            kbrd = kb.main_admin
        else:
            kbrd = kb.main_user
        await message.answer('''🎉 Добро пожаловать в наш телеграм-бот по продажам товаров! ✨ Мы рады видеть тебя здесь! 
                            
    🔎 Ищешь что-то особенное? У нас есть всё: от модной одежды до гаджетов и много другого!

    💬 Если у тебя возникнут вопросы или нужна помощь, просто напиши — мы всегда на связи!

    Начни шопинг уже сейчас и найдите свои идеальные покупки!

    Приятного времяпрепровождения! 🎈''', reply_markup=kbrd)


@router.message(F.text.contains("Мой профиль"))
async def cmd_profile(message: Message):
    user = await rq.get_user(message.from_user.id)
    sum = await rq.get_sum_purschases(message.from_user.id)
    if user.who_invited:
        await message.answer(
            f'🤵\tВаш профиль: \n\n🆔\tВаш id:\t<code>{message.from_user.id}</code> '
            f'\n\n💸\tСумма ваших покупок: {sum}\t₽ \n💳\tВаш баланс: {user.balance}\t₽'
            f'\n\n🤝🏼\tВас пригласил: \t<code>{user.who_invited}</code>'
            f'\n👥\t Количество ваших рефералов: {len(user.referals)}'
            f'\n\n📢\t Ваша реферальная ссылка: t.me/Kaifirikovski_Magazine_bot?start=r_{user.tg_id}',
            parse_mode="HTML", reply_markup = kb.profile_user
        )
    else:
        await message.answer(
            f'🤵\tВаш профиль: \n\n🆔\tВаш id:\t<code>{message.from_user.id}</code> '
            f'\n\n💸\tСумма ваших покупок: {sum}\t₽ \n💳\tВаш баланс: {user.balance}\t₽'
            f'\n\n👥\t Количество ваших рефералов: {len(user.referals)}'
            f'\n📢\t Ваша реферальная ссылка: t.me/Kaifirikovski_Magazine_bot?start=r_{user.tg_id}',
            parse_mode="HTML", reply_markup = kb.profile_user
        )

@router.message(F.text.contains("На главную"))
async def cmd_profile_back(message: Message, state: FSMContext):
    await state.clear()
    user = await rq.get_user(message.from_user.id)
    sum = await rq.get_sum_purschases(message.from_user.id)
    if message.from_user.id in admin_list:
        kbrd = kb.main_admin
    else:
        kbrd = kb.main_user
    await message.answer(
        f'Вы вернулись на главную', 
        reply_markup = kbrd
    )

@router.message(F.text.contains("Товары"))
async def cmd_profile_items(message: Message):
    categories = (await rq.get_categories()).all()
    text_message = ''
    for category in categories:
        items = (await rq.get_items(category.id)).all()
        if items:
            text_message += f'──── <a href="https://t.me/Kaifirikovski_Magazine_bot?start=c_{category.id}">{category.name}</a> ────\n'
            for item in items:
                if (item.amount > 0):
                    text_message += f'<a href="https://t.me/Kaifirikovski_Magazine_bot?start=c_{category.id}_{item.id}">💎\t\t{item.name} - {item.description} | {item.price}₽ | {item.amount} шт.</a>\n'
            text_message += f'\n\n'
    if (text_message):
        await message.answer(text_message, parse_mode = "HTML")
    else:
        await message.answer("Товаров пока нет")

@router.message(F.text.contains("Купить"))
async def cmd_profile_buy(message: Message):
    await message.answer(
        "Выберите категорию, в которой хотите купить товар", 
        reply_markup = await pag.buy_kb_categories()
    )

@router.callback_query(F.data.startswith("back"))
async def buy_category(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите категорию, в которой хотите купить товар", 
        reply_markup = await pag.buy_kb_categories()
    )

@router.callback_query(pag.Buy_category.filter())
async def buy_category(callback: CallbackQuery, callback_data: pag.Buy_category):
    category_id = callback_data.category_id
    await callback.message.edit_text(
        "Выберите название товара", 
        reply_markup= await pag.buy_kb_items(category_id)
    )
    await callback.answer()

@router.callback_query(pag.Buy_item.filter())
async def buy_item(callback: CallbackQuery, callback_data: pag.Buy_item):
    text_message = ''
    category_id = callback_data.category_id
    item_id = callback_data.item_id
    item = await rq.buy_info_item(item_id)
    user = await rq.get_user(callback.from_user.id)
    text_message += f'──── Покупка ────\n\n🛒\tТовар:\t{item.name}\n💰\tЦена:\t{item.price}₽\n📑\tКол-во:\t{item.amount}\n📝\tОписание: {item.description}\n\n💲\tВаш баланс:\t{user.balance}₽'
    
    await callback.message.edit_text(
        text_message, 
        reply_markup = await pag.buy_kb_one__or_many(category_id, item_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("buy_one_item_"))
async def buy_one_item(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split("_")[3])
    item = await rq.buy_info_item(item_id)
    user = await rq.get_user(callback.from_user.id)
    text_message = ''
    if (user.balance - item.price >= 0):
        text_message = f'🛒\tВаша покупка будет стоить {item.price}₽\n💰\tВаш баланс: {user.balance}₽\n\nПодтверждаете покупку?'
        keybrd = await kb.accept_buy_1(item_id)
    else:
        text_message = f'🛒\tВаша покупка будет стоить {item.price}₽\n⛔\tВам не хватает: {item.price-user.balance}₽\n\n'
        keybrd = await kb.deposit()

    await callback.message.answer(
        text_message, 
        reply_markup = keybrd
    )
    await callback.answer()

@router.callback_query(F.data.startswith("buy_more_item_"))
async def buy_many_item(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split("_")[3])
    item = await rq.buy_info_item(item_id)

    await callback.message.answer(
        f"Введите количество товара, которое вы хотите купить."
        f"\n\nМинимальное количество:\t<b>1</b>\nМаксимальное количество:"
        f"\t<b>{item.amount}</b>", parse_mode="HTML"
    )

    await state.set_state(many_items.item)
    await state.update_data(item = item_id)

    await callback.answer()


@router.message(many_items.item)
async def many_buy_item(message: Message, state: FSMContext):
    data = await state.get_data()
    item_count = int(message.text)
    item_id = data['item']
    item = await rq.buy_info_item(item_id)

    if (item_count <= item.amount):
        user = await rq.get_user(message.from_user.id)
        text_message = ''
        if (user.balance - item_count*item.price >= 0):
            text_message = f'🛒\tВаша покупка будет стоить {item_count*item.price}₽\n💰\tВаш баланс: {user.balance}₽\n\nПодтверждаете покупку?'
            keybrd = await kb.accept_buy_many(item_id, item_count)
        else:
            text_message = f'🛒\tВаша покупка будет стоить {item_count*item.price}₽\n⛔\tВам не хватает: {item_count*item.price-user.balance}₽\n\n'
            keybrd = await kb.deposit()
        await message.answer(text_message, reply_markup = keybrd)
        await state.clear()
    else:
        await message.answer(
            f"Такого количества товара нет! Введите количество товара, которое вы хотите купить."
            f"\n\nМинимальное количество:\t<b>1</b>\nМаксимальное количество:"
            f"\t<b>{item.amount}</b>", parse_mode="HTML"
        )



@router.callback_query(F.data.startswith("accept_"))
async def buy_many_item(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[3])
    item_count = int(callback.data.split("_")[1])
    item = await rq.buy_info_item(item_id)
    if item.amount >= item_count:
        product = await rq.buy_item(callback.from_user.id, item_id, item_count)
        text_message = "Ваш товар:\n"
        for item in product:
            text_message += f'{item.data}\n'
        await callback.message.edit_text(text_message)
    else:
        await callback.message.edit_text(f'К сожалению, такого количества товара уже нет.')
    await callback.answer()


@router.message(F.text.contains("История покупок"))
async def cmd_profile_buy(message: Message):
    await message.answer(
        "История ваших покупок", 
        reply_markup = await pag.get_paginated_kb(message.from_user.id)
    )


@router.callback_query(pag.Pagination.filter())
async def products_pagination_callback(callback: CallbackQuery, callback_data: pag.Pagination):
    page = callback_data.page
    await callback.message.edit_text(
        "История ваших покупок", 
        reply_markup=await pag.get_paginated_kb(callback.from_user.id, page)
    )
    

@router.callback_query(pag.ProductData.filter())
async def products_pagination_callback(callback: CallbackQuery, callback_data: pag.ProductData):
    purschase_id = callback_data.purschase_id
    purschase = await rq.get_one_purschase(callback.from_user.id, purschase_id)

    await callback.message.edit_text(
        f'🗓️\tВремя покупки: {purschase.created_at.year}/{purschase.created_at.month:02}/{purschase.created_at.day:02}\t{purschase.created_at.hour:02}:{purschase.created_at.minute:02}:{purschase.created_at.second:02}\n\n'
        f'🆔\tНомер покупки: <code>{purschase_id}</code>\n\n'
        f'📝\tНазвание товара: {purschase.name_of_purschase}\n\n'
        f'💲\tСумма покупки: {purschase.sum_of_purschase}₽\n\n'
        f'📊\tВаши данные: \n\n{purschase.product_of_purschase}',
        reply_markup=await pag.back_to_history(),
        parse_mode="HTML"
    )


@router.message(F.text.contains("Тех. Поддержка"))
async def cmd_profile_buy(message: Message, state: FSMContext):
    if await rq.get_apeal(message.from_user.id):
        await message.answer("Ваше прошлое обращение ещё в обработке!")
    else:
        await message.answer("Напишите, что у вас случилось (максимум 250 символов)")
        await state.set_state(appeals.appeal)


@router.message(appeals.appeal)
async def cmd_profile_buy(message: Message, state: FSMContext):
    if len(message.text) <= 250:
        await rq.add_apeal(message.from_user.id, message.text)
        await message.answer("Сообщение успешно отправлено!")
        await state.clear()
    else:
        await message.answer("В сообщении должно быть не более 250 символвов!")


@router.callback_query(F.data == "check_subcr")
async def check_subcr(callback: CallbackQuery):
    sub = await bot.get_chat_member(chat_id = -1002263423567, user_id = callback.from_user.id)
    if sub.status != "left":
        await callback.message.edit_text("Вы успешно подписались на канал!")
    await callback.answer()
