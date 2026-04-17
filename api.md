# API сервиса книг

## Общая информация

- Фреймворк: FastAPI
- Базовый URL (локально): `http://localhost:8000`
- OpenAPI схема: `GET /openapi.json`
- Swagger UI: `GET /docs`
- ReDoc: `GET /redoc`
- Во все ответы middleware добавляет заголовок `X-Process-Time` (в секундах)

## Модель данных

### Book

```json
{
  "id": 1,
  "title": "string",
  "author": "string",
  "content": "string"
}
```

## Эндпоинты

### `GET /`

Базовый сервисный эндпоинт.

- Ответ: `200 OK`

```json
{
  "message": "index"
}
```

### `POST /books/`

Создать книгу.

- Тело запроса:

```json
{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "content": "In a hole in the ground there lived a hobbit..."
}
```

- Ответ: `201 Created`

```json
{
  "id": 1,
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "content": "In a hole in the ground there lived a hobbit..."
}
```

- Ошибки:
- `422 Unprocessable Entity` при невалидном теле запроса.

### `GET /books/`

Получить список всех книг (сортировка по `id` по возрастанию).

- Ответ: `200 OK`

```json
[
  {
    "id": 1,
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien"
  }
]
```

### `GET /books/{book_id}`

Получить книгу по идентификатору.

- Path-параметры:
- `book_id` (`int`) — идентификатор книги.

- Ответ: `200 OK`

```json
{
  "id": 1,
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "content": "In a hole in the ground there lived a hobbit..."
}
```

- Ошибки:
- `404 Not Found`

```json
{
  "detail": "Book not found"
}
```

- `422 Unprocessable Entity` при невалидном `book_id`.

### `PATCH /books/{book_id}`

Частично обновить книгу.

- Path-параметры:
- `book_id` (`int`) — идентификатор книги.

- Тело запроса (все поля опциональны):

```json
{
  "title": "The Hobbit (updated)",
  "author": "J.R.R. Tolkien",
  "content": "Updated content"
}
```

Если передать пустой объект `{}`, вернётся текущая версия книги без изменений.

- Ответ: `200 OK`

```json
{
  "id": 1,
  "title": "The Hobbit (updated)",
  "author": "J.R.R. Tolkien",
  "content": "Updated content"
}
```

- Ошибки:
- `404 Not Found`

```json
{
  "detail": "Book not found"
}
```

- `422 Unprocessable Entity` при невалидном теле запроса или `book_id`.

### `DELETE /books/{book_id}`

Удалить книгу по идентификатору.

- Path-параметры:
- `book_id` (`int`) — идентификатор книги.

- Ответ: `204 No Content` (пустое тело)

- Ошибки:
- `404 Not Found`

```json
{
  "detail": "Book not found"
}
```

- `422 Unprocessable Entity` при невалидном `book_id`.

## Примечания

- Авторизация в текущих роутерах не используется.
- CORS включён и настраивается через переменные окружения/настройки.
