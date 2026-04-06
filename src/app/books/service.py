from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.models import Book
from app.books.schemas import BookCreateSchema, BookUpdateSchema


class BookService:
    async def create_book(
        self, session: AsyncSession, book_data: BookCreateSchema
    ) -> Book:
        stmt = insert(Book).values(**book_data.model_dump()).returning(Book)
        result = await session.execute(stmt)
        return result.scalar_one()

    async def get_book_by_id(
        self, session: AsyncSession, book_id: int
    ) -> Book | None:
        stmt = select(Book).where(Book.id == book_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_books(self, session: AsyncSession) -> list[Book]:
        stmt = select(Book).order_by(Book.id)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def update_book(
        self, session: AsyncSession, book_id: int, book_data: BookUpdateSchema
    ) -> Book | None:
        values = book_data.model_dump(exclude_unset=True)
        if not values:
            return await self.get_book_by_id(session, book_id)

        stmt = (
            update(Book)
            .where(Book.id == book_id)
            .values(**values)
            .returning(Book)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_book(self, session: AsyncSession, book_id: int) -> bool:
        stmt = delete(Book).where(Book.id == book_id).returning(Book.id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None
