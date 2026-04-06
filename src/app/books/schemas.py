from pydantic import BaseModel, ConfigDict


class BookBaseSchema(BaseModel):
    title: str
    author: str
    content: str


class BookCreateSchema(BookBaseSchema):
    pass


class BookUpdateSchema(BaseModel):
    title: str | None = None
    author: str | None = None
    content: str | None = None


class BookReadSchema(BookBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
