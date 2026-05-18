from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BooksModel
from schemas.books import SBookAdd


class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd, session: AsyncSession) -> BooksModel:
        book = BooksModel(**data.model_dump())

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def find_all(cls, session: AsyncSession) -> list[BooksModel]:
        result = await session.execute(select(BooksModel))
        return result.scalars().all()

    @classmethod
    async def find_by_id(cls, book_id: int, session: AsyncSession) -> BooksModel | None:
        result = await session.execute(
            select(BooksModel).where(BooksModel.id == book_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def update_one(cls, book_id: int, data: SBookAdd, session: AsyncSession) -> BooksModel | None:
        result = await session.execute(
            select(BooksModel).where(BooksModel.id == book_id)
        )
        book = result.scalar_one_or_none()

        if book is None:
            return None

        for key, value in data.model_dump().items():
            setattr(book, key, value)

        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def delete_one(cls, book_id: int, session: AsyncSession) -> bool:
        result = await session.execute(
            delete(BooksModel).where(BooksModel.id == book_id)
        )

        await session.commit()

        return result.rowcount > 0