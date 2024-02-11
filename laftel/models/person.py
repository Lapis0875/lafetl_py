from pydantic_core import Url
from .base import LaftelObject, LaftelDBEntry

__all__ = ("PartialPersonInfo", "PersonInfo")
    
class PartialPersonInfo(LaftelObject):
    """라프텔에서 표기하는 간단한 인물 정보를 나타냅니다."""
    name: str
    img: Url

class PersonInfo(LaftelDBEntry):
    """라프텔에서 표기하는 인물 정보를 나타냅니다."""
    content: str
    img: Url
    job: str
    name: str
    status: bool
    url: Url | None
