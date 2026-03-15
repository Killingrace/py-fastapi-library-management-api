from datetime import date
from pydantic import BaseModel
from db.models import AuthorORM, BookORM






class AuthorAddDTO(BaseModel):
    name: str
    bio: str


class AuthorDTO(AuthorAddDTO):
    id: int



class BookAddDTO(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookDTO(BookAddDTO):
    id: int


class AuthorRelDTO(AuthorDTO):
    books: list["BookDTO"]


class BookRelDTO(BookDTO):
    author: "AuthorDTO"
