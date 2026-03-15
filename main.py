from typing import Annotated
from uvicorn import run
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.database import SessionCreator
import crud
from schemas import AuthorDTO, AuthorAddDTO, BookDTO, BookAddDTO, AuthorRelDTO, BookRelDTO


app = FastAPI()

def get_db():
    db = SessionCreator()
    try:
        yield db
    finally:
        db.close()


@app.post("/author/", response_model=AuthorDTO)
def new_author(
    new_author: AuthorAddDTO,
    db: Annotated[Session, Depends(get_db)]
):
    check_if_author_exists = crud.select_author_by_name(db=db, name=new_author.name)
    if check_if_author_exists:
        raise HTTPException(status_code=400, detail="Author with same name already exists!")
    return crud.create_author(
        db=db,
        new_author=new_author
    )


@app.get("/author/{author_id}", response_model=AuthorRelDTO)
def get_single_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    selected_author = crud.read_single_author(db=db, author_id=author_id)
    if not selected_author:
        raise HTTPException(status_code=404, detail="Author not found!")
    return selected_author


@app.get("/author_page/{skip}-{limit}", response_model=list[AuthorRelDTO])
def get_list_of_authors(
    skip: int,
    limit: int,
    db: Annotated[Session, Depends(get_db)]
):
    return crud.select_authors(db=db, skip=skip, limit=limit)



@app.post("/book/", response_model=BookRelDTO)
def new_book(
    new_book: BookAddDTO,
    db: Annotated[Session, Depends(get_db)]
):
    book_author = crud.read_single_author(db=db, author_id=new_book.author_id)
    if not book_author:
        raise HTTPException(status_code=404, detail="Author with same id dont exists")
    return crud.create_book(db=db, new_book=new_book)


@app.get("/book/{author_id}", response_model=list[BookDTO])
def get_books_by_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    author = crud.read_single_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author.books

@app.get("/book_page/{skip}-{limit}", response_model=list[BookRelDTO])
def get_list_of_books(
    skip: int,
    limit: int,
    db: Annotated[Session, Depends(get_db)]
):
    return crud.select_books(db=db, skip=skip, limit=limit)



if __name__=="__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=True)