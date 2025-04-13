from typing import Any, Dict, cast

import boto3
from chalice.app import BadRequestError, Chalice, Request

from chalicelib.models import Book, BookCreate
from chalicelib.repository import BookRepository

app = Chalice(app_name="inventory_service")
dynamodb = boto3.resource("dynamodb")
repo = BookRepository(dynamodb)


@app.route("/books", methods=["POST"])
def create_book() -> Dict[str, Any]:
    try:
        request = cast(Request, app.current_request)
        book_data: Dict[str, Any] = request.json_body
        book_create = BookCreate(**book_data)
        book: Book = repo.create_book(book_create)
        return book.model_dump(mode="json")
    except ValueError as e:
        raise BadRequestError(str(e))
