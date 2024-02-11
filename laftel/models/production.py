from pydantic_core import Url 
from .base import LaftelObject

__all__ = ("Production", )

class Production(LaftelObject):
    """라프텔의 제작사 정보를 나타냅니다."""
    name: str
    img: Url
