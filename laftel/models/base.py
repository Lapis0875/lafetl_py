from pydantic import BaseModel, NonNegativeInt
from datetime import datetime

__all__ = ("LaftelObject", "LaftelDBEntry")

class LaftelObject(BaseModel):
    """라프텔 내부 객체들 중, id를 가지는 객체들의 공통 조상."""
    id: NonNegativeInt

class LaftelDBEntry(LaftelObject):
    """라프텔 내부 객체들 중, DB 관련 필드를 가지는 객체들의 공통 조상."""
    created: datetime
    modified: datetime
