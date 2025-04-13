import re
from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class BookBase(BaseModel):
    """Base model with common book attributes"""

    title: str
    authors: List[str]
    publisher: str
    publication_date: date
    price: Decimal = Field(gt=0)
    categories: List[str]
    description: Optional[str] = None
    stock_quantity: int = Field(ge=0, default=0)
    status: str = "active"

    @validator("price", pre=True)
    def parse_price(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        if isinstance(v, str):
            return Decimal(v)
        return v

    @validator("price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v.quantize(Decimal("0.01"))

    class Config:
        json_enconders = {Decimal: lambda v: float(v)}


class BookCreate(BookBase):
    """Model for creating a new book"""

    isbn: str

    @validator("isbn")
    def validate_isbn(cls, v):
        """Simple validation for ISBN-13 format"""

        if not re.match(r"^\d{13}$", v):
            raise ValueError("ISBN must be a valid 13-digit number")
        return v


class BookUpdate(BookBase):
    """Model for updating an existing book"""

    title: Optional[str] = None
    authors: Optional[List[str]] = None
    publisher: Optional[str] = None
    publication_date: Optional[date] = None
    price: Optional[float] = None
    categories: Optional[List[str]] = None
    description: Optional[str] = None
    stock_quantity: Optional[int] = None
    status: Optional[str] = None

    @validator("price")
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than zero")
        return round(v, 2) if v is not None else v


class StockUpdate(BaseModel):
    """Model for updating just the stock quantity"""

    stock_quantity: int = Field(ge=0)


class Book(BookBase):
    """Complete book model with identifier"""

    isbn: str
