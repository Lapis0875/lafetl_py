from pydantic import BaseModel, PositiveInt
from .enums import LaftelTagTypes

__all__ = ("LaftelTag",)

class LaftelTag(BaseModel):
    """라프텔에 사용되는 태그를 나타냅니다."""
    id: PositiveInt
    is_show: bool
    name: str
    type: LaftelTagTypes