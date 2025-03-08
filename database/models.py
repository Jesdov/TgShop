from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import String, BigInteger, ForeignKey, func, ARRAY

from datetime import datetime

from typing import List, Optional

from config import URL



engine = create_async_engine(URL)

async_session = async_sessionmaker(bind = engine, expire_on_commit= False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, unique=True)
    balance: Mapped[int] = mapped_column(default = 0)
    who_invited: Mapped[Optional[BigInteger]] = mapped_column(BigInteger)
    referals: Mapped[List[BigInteger]] = mapped_column(ARRAY(BigInteger), default=list)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

class User_appeal(Base):
    __tablename__ = "user_appeals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    appeal : Mapped[str] = mapped_column(String(250))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, ForeignKey("users.tg_id"))

class Ban_user(Base):
    __tablename__ = "ban_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class purchase(Base):
    __tablename__ = "users_purchases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    sum_of_purschase : Mapped[int] = mapped_column()
    name_of_purschase: Mapped[str] = mapped_column()
    product_of_purschase: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

class category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25))
    items: Mapped[List["item"]] = relationship("item", back_populates = "category_", cascade="all, delete")

class item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column()
    amount: Mapped[int] = mapped_column(default = 0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category_: Mapped["category"] = relationship("category", back_populates = "items")
    products: Mapped[List["product_data"]] = relationship("product_data", back_populates = "item_", cascade="all, delete")


class product_data(Base):
    __tablename__ = "product_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data: Mapped[str] = mapped_column(String(100))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    item_: Mapped["item"] = relationship("item", back_populates = "products")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)