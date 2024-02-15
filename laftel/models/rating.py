from datetime import date
from pydantic import BaseModel

__all__ = ("Rating",)

class Rating(BaseModel):
    """국내 심의 정보"""
    broadcast_channel_name: str
    broadcast_date: date | None
    classification_number: str
    rating: int | None
    rating_components: list
