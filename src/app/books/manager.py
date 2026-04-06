from app.books.models import Book
from app.books.schemas import BookCreateSchema, BookUpdateSchema
from app.books.service import BookService
from sqlalchemy.ext.asyncio import AsyncSession


class BookManager:
    def __init__(self) -> None:
        self.service = BookService()

    async def create_book(
        self, session: AsyncSession, book_data: BookCreateSchema
    ) -> Book:
        try:
            book = await self.service.create_book(session, book_data)
            await session.commit()
            return book
        except Exception:
            await session.rollback()
            raise

    async def get_book_by_id(
        self, session: AsyncSession, book_id: int
    ) -> Book | None:
        return await self.service.get_book_by_id(session, book_id)

    async def get_books(self, session: AsyncSession) -> list[Book]:
        return await self.service.get_books(session)

    async def update_book(
        self, session: AsyncSession, book_id: int, book_data: BookUpdateSchema
    ) -> Book | None:
        try:
            updated_book = await self.service.update_book(session, book_id, book_data)
            await session.commit()
            return updated_book
        except Exception:
            await session.rollback()
            raise

    async def delete_book(self, session: AsyncSession, book_id: int) -> bool:
        try:
            is_deleted = await self.service.delete_book(session, book_id)
            await session.commit()
            return is_deleted
        except Exception:
            await session.rollback()
            raise
