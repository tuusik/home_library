from fastapi import APIRouter, HTTPException, status
from schemas.books import SBook, SBookAdd

router = APIRouter(prefix="/books")

@router.post("", status_code=status.HTTP_201_CREATED)
async def add_new_book(book: SBookAdd) -> SBook:
    return {"result": "Книга добавлена!"}

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_books() -> list[SBook]:
    return {"result": "Вот все книги: "}

@router.get("/{id}")
async def get_book(id: int) -> SBook:
    if id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return db[id]

@router.put("/{id}")
async def update_book(id: int, book: SBookAdd) -> SBook:
    if id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    db[id] = book
    return db[id]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int) -> None:
    if id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del db[id]

