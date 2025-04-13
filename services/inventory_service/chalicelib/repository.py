from decimal import Decimal

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from .models import Book, BookCreate


class BookRepository:
    def __init__(self, dynamodb_resource):
        self.table = dynamodb_resource.Table("books")

    def create_book(self, book: BookCreate) -> Book:
        """
        Create a new book in DynamoDB.
        Args:
            book: BookCreate object with book details including isbn.
        Returns:
            Book object with stored details.
        Raises:
            ValueError: If ISBN already exists.
        """
        item = {
            "isbn": book.isbn,
            "title": book.title,
            "authors": book.authors,
            "publisher": book.publisher,
            "publication_date": book.publication_date.isoformat(),
            "price": book.price,
            "categories": book.categories,
            "description": book.description,
            "stock_quantity": book.stock_quantity,
            "status": book.status,
        }
        try:
            self.table.put_item(
                Item=item, ConditionExpression="attribute_not_exists(isbn)"
            )
        except ClientError as e:
            if (
                e.response["Error"]["Code"]
                == "ConditionalCheckFailedException"
            ):
                raise ValueError(f"Book with ISBN {book.isbn} already exists")
            raise
        return Book(**item)
