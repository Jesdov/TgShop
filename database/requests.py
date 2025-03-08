from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove


from database.models import async_session
from database.models import User, purchase, category, item, product_data, User_appeal
from sqlalchemy import select, update, delete, func, literal
from sqlalchemy import String, BigInteger


async def set_user(tg_id: BigInteger, who_invited: BigInteger = 0):
    async with async_session() as session:
        if who_invited == 0:
            session.add(User(tg_id = tg_id))
        else:
            user_who_invited = await get_user(who_invited)
            if (user_who_invited):
                session.add(User(tg_id = tg_id, who_invited = who_invited))
                stmt = update(User).where(User.tg_id == who_invited).values(referals = User.referals + [tg_id])
                await session.execute(stmt)
        await session.commit()


async def get_user(tg_id: BigInteger):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))
    

async def get_sum_purschases(tg_id: BigInteger):
    async with async_session() as session:
        purschases = (await session.scalars(select(func.sum(purchase.sum_of_purschase)).where(purchase.tg_id == tg_id))).first()
        if purschases:
            return purschases
        else:
            return 0
        
async def add_category(name: String):
    async with async_session() as session:
        categories = (await session.scalars(select(category).where(category.name == name))).first()
        if categories:
            return 0
        else:
            session.add(category(name = name)) 
            await session.commit()
            return 1
        
async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(category))
    
    
async def add_item(name: String, description: String, price: int, id: int):
    async with async_session() as session:
        items = (await session.scalars(select(item).where(item.name == name, item.description == description, item.price == price))).first()
        if items:
            return 0
        else:
            session.add(item(name = name, description = description, price = price, category_id = id)) 
            await session.commit()
            return 1
        
async def get_items(category_id: int):
    async with async_session() as session:
        return await session.scalars(select(item).where(item.category_id == category_id))

async def add_product_of_item(item_id: int, data: list):
    async with async_session() as session:
        product_objects = [product_data(data=prod, item_id=item_id) for prod in data]
        session.add_all(product_objects)
        await session.commit()
        stmt = update(item).where(item.id == item_id).values(amount = item.amount + len(data))
        await session.execute(stmt)
        await session.commit()


async def delete_category(category_id: int):
    async with async_session() as session:
        categor = await session.get(category, category_id)
        await session.delete(categor)
        await session.commit()
        

async def delete_item(item_id: int):
    async with async_session() as session:
        itemdel = await session.get(item, item_id)
        await session.delete(itemdel)
        await session.commit()



async def info_item(item_id: int):
    async with async_session() as session:
        category_id = await session.scalar(select(item.category_id).where(item.id == item_id))
        result = await session.execute(
            select(category.name, item.name, item.description)
            .join(item, item.category_id == category.id)
            .where(item.id == item_id)
        )
        return result.fetchone()
    
async def get_products_of_item(item_id: int):
    async with async_session() as session:
        return (await session.scalars(select(product_data).where(product_data.item_id == item_id)))
    


async def delete_product(item_id: int, product_id: int):
    async with async_session() as session:
            async with async_session() as session:
                stmt = delete(product_data).where(product_data.item_id == item_id, product_data.id == product_id)
                await session.execute(stmt)

                stmt = update(item).where(item.id == item_id).values(amount = item.amount - 1)
                await session.execute(stmt)

                await session.commit()

async def delete_all_product(item_id: int):
    async with async_session() as session:
            async with async_session() as session:
                stmt = delete(product_data).where(product_data.item_id == item_id)
                await session.execute(stmt)

                stmt = update(item).where(item.id == item_id).values(amount = 0)
                await session.execute(stmt)

                await session.commit()


async def buy_info_item(item_id: int):
    async with async_session() as session:
        return await session.scalar(select(item).where(item.id == item_id))
    
async def buy_item(user_id: int, item_id: int, count: int):
    async with async_session() as session:
        result = await (session.scalars(select(product_data)
                          .where(product_data.item_id == item_id)
                          .limit(count)))
        product_to_delete = result.all()
        if product_to_delete:
            prd_to_del = [product.id for product in product_to_delete]

            stmt = delete(product_data).where(product_data.id.in_(prd_to_del))
            await session.execute(stmt)

        stmt = update(item).where(item.id == item_id).values(amount = item.amount - count)
        await session.execute(stmt)

        price = await session.scalar(select(item.price).where(item.id == item_id))
        stmt = update(User).where(User.tg_id == user_id).values(balance = User.balance - count*price)
        await session.execute(stmt)

        text = ''
        for product in product_to_delete:
            text += f'{product.data}, '

        result = await (session.scalar(select(item.name)
                          .where(item.id == item_id)))
        
        session.add(purchase(tg_id = user_id, sum_of_purschase = count*price, name_of_purschase = result, product_of_purschase = text))

        who_invited = await (session.scalar(select(User.who_invited)
                          .where(User.tg_id == user_id)))
        if who_invited:
            stmt = update(User).where(User.tg_id == who_invited).values(balance = User.balance + count*price/20)
            await session.execute(stmt)

        await session.commit()
        
        return product_to_delete


async def get_purschases(user_id: int):
    async with async_session() as session:
        return (await session.scalars(select(purchase).where(purchase.tg_id == user_id))).all()
    
async def get_one_purschase(user_id: int, purschase_id: int):
    async with async_session() as session:
        return await session.scalar(select(purchase).where(purchase.tg_id == user_id, purchase.id == purschase_id))
    
async def add_apeal(user_id: int, appeal: str):
    async with async_session() as session:
        session.add(User_appeal(tg_id = user_id, appeal = appeal))
        await session.commit()

async def get_apeals():
    async with async_session() as session:
        result = await session.scalars(select(User_appeal))
        return result.all()
    
async def get_apeal(user_id: int):
    async with async_session() as session:
        result = await session.scalars(select(User_appeal).where(User_appeal.tg_id == user_id))
        return result.all()
    
async def get_apeal_for_id(appeal_id: int):
    async with async_session() as session:
        result = await session.scalar(select(User_appeal).where(User_appeal.id == appeal_id))
        return result
    
async def del_apeal(appeal_id: int):
    async with async_session() as session:
        stmt = delete(User_appeal).where(User_appeal.id == appeal_id)
        await session.execute(stmt)
        await session.commit()
    
async def get_tg_all():
    async with async_session() as session:
        result = await session.scalars(select(User.tg_id))
        return result.all()