from sqlalchemy import select, and_
from sqlalchemy.orm import Session, selectinload, joinedload
from db.models import AuthorORM, BookORM
from schemas import AuthorAddDTO, AuthorDTO, BookAddDTO, BookDTO


def make_indexes(page):
    return ((page - 1) * 5, page * 5)


def create_author(db: Session, new_author: AuthorAddDTO) -> AuthorORM:
    new_db_author = AuthorORM(
        name=new_author.name,
        bio=new_author.bio
    )
    db.add(new_db_author)
    db.commit()
    db.refresh(new_db_author)

    return new_db_author


def read_single_author(db: Session, author_id: int) -> AuthorORM | None:
    query = (
        select(AuthorORM)
        .where(AuthorORM.id == author_id)
        .options(selectinload(AuthorORM.books))
    )
    return db.execute(query).scalars().first()


def select_authors(db: Session, page: int) -> list[AuthorORM] | None:
    start, top = make_indexes(page)
    query = (
        select(AuthorORM)
        .offset(start)
        .limit(top)
        .options(selectinload(AuthorORM.books))
    )
    return db.execute(query).scalars().all() # type: ignore


def select_author_by_name(db: Session, name: str) -> AuthorORM | None:
    query = (
        select(AuthorORM)
        .where(
            AuthorORM.name == name
        )
        .options(selectinload(AuthorORM.books))
    )
    return db.execute(query).scalars().first()

def create_book(db: Session, new_book: BookAddDTO) -> BookORM:
    new_book_db = BookORM(
        title=new_book.title,
        summary=new_book.summary,
        publication_date=new_book.publication_date,
        author_id=new_book.author_id
    )
    db.add(new_book_db)
    db.commit()
    db.refresh(new_book_db)

    return new_book_db


def read_books_by_author(db: Session, author_id: int) -> list[BookORM]:
    query = (
        select(BookORM)
        .where(BookORM.author_id == author_id)
        .options(joinedload(BookORM.author))
    )
    return db.execute(query).scalars().all() # type: ignore


def select_books(db: Session, page: int) -> list[BookORM]:
    start, top = make_indexes(page)
    query = (
        select(BookORM)
        .offset(start)
        .limit(top)
        .options(joinedload(BookORM.author))
    )
    return db.execute(query).scalars().all() # type: ignore
