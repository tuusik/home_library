from fastapi import APIRouter, HTTPException, status
from repository import BookRepository
from schemas.books import SBook, SBookAdd
from database import SessionDep

router = APIRouter(prefix="/books")

@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def add_new_book(book: SBookAdd, session: SessionDep) -> SBook:
    return await BookRepository.add_one(book, session)


@router.get("", response_model=list[SBook])
async def get_all_books(session: SessionDep) -> list[SBook]:
    return await BookRepository.find_all(session)


@router.get("/{id}", response_model=SBook)
async def get_book(id: int, session: SessionDep) -> SBook:
    book = await BookRepository.find_by_id(id, session)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return book


@router.put("/{id}", response_model=SBook)
async def update_book(id: int, new_book: SBookAdd, session: SessionDep) -> SBook:
    book = await BookRepository.update_one(id, new_book, session)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int, session: SessionDep):
    deleted = await BookRepository.delete_one(id, session)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )