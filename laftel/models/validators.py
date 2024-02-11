from typing import Annotated, Callable, TypeVar, TypeAliasType
from pydantic import AfterValidator, GetCoreSchemaHandler

__all__ = ("Handler", "YearString", "Year", "SeasonString", "Season")

T = TypeVar("T")
Handler = TypeAliasType("Handler", Callable[[T, GetCoreSchemaHandler], T], type_params=(T,))

# 'XXXX년' 형식의 문자열을 검증합니다.
def validate_year(v: str) -> str:
    """'XXXX년', 'XXXX년 X분기', 'XXXX년 X분기|XXXX년 Y분기' 같은 형식의 문자열을 검증합니다.
    
    Args:
        v (str): 검증할 문자열.
    
    Returns:
        str: 검증된 문자열.
    
    Raises:
        ValueError: 문자열이 'XXXX년', 'XXXX년 X분기', 'XXXX년 X분기|XXXX년 Y분기' 형식이 아닐 경우 발생합니다.
    """
    if not isinstance(v, str):      # 문자열이 아닌 경우에는 검증을 하지 않습니다.
        return v
    
    quarters: list[str] = v.split("|")
    for q in quarters:
        parts: list[str] = q.split(" ")
        if not parts[0].endswith("년"):
            print(f"Validators > !!{q}의 연도 부분인 {parts[0]}는 '년'으로 끝나지않음!!")
            raise ValueError(f"Invalid air year quarter value: {v}\n : lacks '년' at the end of year expression.")
        elif len(parts) == 2 and not parts[1].endswith("분기"):
            raise ValueError(f"Invalid air year quarter value: {v}\n : lacks '분기' at the end of quarter expression.")
        elif not parts[0][:-1].isdecimal() or (len(parts) == 2 and not parts[1][:-2].isdecimal()):
            raise ValueError(f"Invalid air year quarter value: {v}\n : Only number can be used to describe year or quarter.")
    return v        
    
YearString: AfterValidator = AfterValidator(validate_year)
Year = TypeAliasType("Year", Annotated[str, YearString])

# '시즌 X' 형식의 문자열을 검증합니다.
def validate_season(v: str) -> str:
    """'시즌 X' 형식의 문자열을 검증합니다.
    
    Args:
        v (str): 검증할 문자열.
    
    Returns:
        str: 검증된 문자열.
    
    Raises:
        ValueError: 문자열이 '시즌 X' 형식이 아닐 경우 발생합니다.
    """
    if not isinstance(v, str):
        return v
    
    if not v.startswith("시즌"):
        raise ValueError(f"Invalid season value: {v}\n : lacks '시즌' at the beginning of season expression.")
    elif not v[3:].isdecimal():
        raise ValueError(f"Invalid season value: {v}\n : Only number can be used to describe season.")
    
    return v

SeasonString: AfterValidator = AfterValidator(validate_season)
Season = TypeAliasType("Season", Annotated[str, SeasonString])

# '시즌 X' 형식의 문자열을 검증합니다.
# // 왜 쿨을 Cours라고 적어둔걸까요?
def validate_cours(v: str) -> str:
    """'X쿨' 형식의 문자열을 검증합니다.
    
    Args:
        v (str): 검증할 문자열.
    
    Returns:
        str: 검증된 문자열.
    
    Raises:
        ValueError: 문자열이 'X쿨' 형식이 아닐 경우 발생합니다.
    """
    if not isinstance(v, str):
        return v
    
    if not v.endswith("쿨"):
        raise ValueError(f"Invalid season value: {v}\n : lacks '쿨' at the end of cours expression.")
    elif not v[:-1].isdecimal():
        raise ValueError(f"Invalid season value: {v}\n : Only number can be used to describe cours.")
        
    return v
CoursString: AfterValidator = AfterValidator(validate_cours)
Cours = TypeAliasType("Cours", Annotated[str, CoursString])
