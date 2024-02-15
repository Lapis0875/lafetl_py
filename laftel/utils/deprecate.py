from typing import TypeAliasType
import typing_extensions
import warnings
from functools import wraps

Version = TypeAliasType("Version", tuple[int, int])

class LaftelDeprecationWarning(DeprecationWarning):
    """lafte.py 라이브러리의 특정 기능이 더 이상 지원되지 않음을 알리는 경고 객체입니다."""
    message: str
    
    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.message = message.rstrip(".")
    
    def __str__(self) -> str:
        return self.message

def deprecated(since: Version, expected_removal: Version, substitute: str = ""):
    """Mark decorated function to be deprecated.
    
    Args:
        since (tuple[int, int]): The version in which the decorated function was implemented.
        expected_removal (tuple[int, int]): The version in which the decorated function will be removed.
        substitute (str): The name of substitute function if exist. Default is "".
    """
    def decorator(func):
        msg: str = (
            f"The `{func.__name__}` method is deprecated; use `{substitute}` instead."
            f"Deprecated in laftel.py V{since[0]}.{since[1]} to be removed in V{expected_removal[0]}.{expected_removal[1]}."
        )
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, category=LaftelDeprecationWarning)
            return func(*args, **kwargs)
        return typing_extensions.deprecated(msg, category=None)(wrapper)
    return decorator