from fastapi import APIRouter, HTTPException
from schemas.books import SBook, SBookAdd

router = APIRouter(prefix="/books")

@router.post("", status_code=201)
def add_new_book(book: SBookAdd) -> SBook:
    return {"result": "Книга добавлена!"}

@router.get("", status_code=200)
def get_all_books() -> list[SBook]:
    return {"result": "Вот все книги: "}

@router.get("/{id}")
def get_book(id: int) -> SBook:
    if id not in db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return db[id]

@router.put("/{id}")
def update_book(id: int, book: SBookAdd) -> SBook:
    if id not in db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    db[id] = book
    return db[id]

@router.delete("/{id}", status_code=204)
def delete_book(id: int) -> None:
    if id not in db:
        raise HTTPException(status_code=404)
    del db[id]

