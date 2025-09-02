import re
from datetime import date, datetime
from typing import Optional, Any

from pydantic import BaseModel, HttpUrl, field_validator

class ArticleModel(BaseModel):
    title: str
    link: HttpUrl
    publication_date: Optional[date] = None
    author: Optional[str] = None
    source: str
    content: Optional[str] = None

    @field_validator("publication_date", mode='before')
    @classmethod
    def parse_publication_date(cls, value: Any) -> Optional[date]:
        """Accepts a date object directly or parses a date from a string."""
        if value is None:
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value.strip(), "%d %b %Y").date()
            except (ValueError, TypeError):
                try:
                    return date.fromisoformat(value)
                except (ValueError, TypeError):
                    return None
        return None


class CarReviewModel(BaseModel):
    title: str
    link: HttpUrl
    source: str
    publication_date: Optional[date] = None
    author: Optional[str] = None
    verdict: Optional[str] = None
    price: Optional[int] = None
    rating: Optional[float] = None

    @field_validator('title', 'source')
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Field must not be empty or whitespace")
        return stripped

    # FIXED: Corrected the typo from @field_gvalidator to @field_validator
    @field_validator('price', mode='before')
    @classmethod
    def parse_price(cls, value: Any) -> Optional[int]:
        if value is None:
            return None
        price_str = str(value)
        digits = re.sub(r'\D', '', price_str)
        if digits:
            return int(digits)
        return None

    @field_validator('rating', mode='before')
    @classmethod
    def parse_rating(cls, value: Any) -> Optional[float]:
        """Extracts a numeric rating from a string OR validates a float."""
        if value is None:
            return None
        if isinstance(value, (float, int)):
            return float(value)
        if isinstance(value, str):
            match = re.search(r'(\d+\.\d+|\d+)', value)
            if match:
                return float(match.group(1))
        return None