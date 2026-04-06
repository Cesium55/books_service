from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.manager import BookManager
from app.books.schemas import BookCreateSchema, BookReadSchema, BookUpdateSchema
from basic_utils.database import get_async_session_generator


router = APIRouter(prefix="/books", tags=["books"])
manager = BookManager()


@router.post(
    "/",
    response_model=BookReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    book_data: BookCreateSchema,
    session: AsyncSession = Depends(get_async_session_generator),
) -> BookReadSchema:
    book = await manager.create_book(session, book_data)
    return BookReadSchema.model_validate(book)


@router.get("/", response_model=list[BookReadSchema])
async def get_books(
    session: AsyncSession = Depends(get_async_session_generator),
) -> list[BookReadSchema]:
    books = await manager.get_books(session)
    return [BookReadSchema.model_validate(book) for book in books]


@router.get("/{book_id}", response_model=BookReadSchema)
async def get_book_by_id(
    book_id: int,
    session: AsyncSession = Depends(get_async_session_generator),
) -> BookReadSchema:
    book = await manager.get_book_by_id(session, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return BookReadSchema.model_validate(book)


@router.patch("/{book_id}", response_model=BookReadSchema)
async def update_book(
    book_id: int,
    book_data: BookUpdateSchema,
    session: AsyncSession = Depends(get_async_session_generator),
) -> BookReadSchema:
    book = await manager.update_book(session, book_id, book_data)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return BookReadSchema.model_validate(book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_async_session_generator),
) -> Response:
    is_deleted = await manager.delete_book(session, book_id)
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
