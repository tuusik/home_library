from fastapi import APIRouter, HTTPException, status

from models.books import BooksModel
from schemas.books import SBook, SBookAdd
from database import SessionDep
from sqlalchemy import select, delete, update

router = APIRouter(prefix="/books")

@router.post("", status_code=status.HTTP_201_CREATED)
async def add_new_book(book: SBookAdd, session: SessionDep) -> SBook:
    new_book = BooksModel(**book.model_dump())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_books(session: SessionDep) -> list[SBook]:
    query = select(BooksModel)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/{id}", response_model=SBook)
async def get_book(id: int, session: SessionDep) -> SBook:
    query = select(BooksModel).where(BooksModel.id == id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return book

@router.put("/{id}", response_model=SBook)
async def update_book(id: int, new_book: SBookAdd, session: SessionDep) -> SBook:
    query = select(BooksModel).where(BooksModel.id == id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    await session.execute(
        update(BooksModel)
        .where(BooksModel.id == id)
        .values(**new_book.model_dump())
    )

    await session.commit()
    await session.refresh(book)
    return book

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int, session: SessionDep) -> None:
    result = await session.execute(
        delete(BooksModel).where(BooksModel.id == id)
    )

    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return