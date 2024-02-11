from enum import StrEnum, auto

__all__ = ("LaftelObjectTypes", "LaftelTagTypes", "Medium", "ContentRating", "Weekdays")

class LaftelObjectTypes(StrEnum):
    """라프텔의 모델 타입을 나타냅니다."""
    animation = auto()
    comics = auto()

class LaftelTagTypes(StrEnum):
    """라프텔의 모델 타입을 나타냅니다."""
    NORMAL = DEFAULT = "일반"
    GENRE = "장르"
    ONE_LINE_REVIEW = "한줄평"

class Medium(StrEnum):
    """방영 유형을 나타냅니다."""
    TVA = "TVA"
    OVA = "OVA"

class ContentRating(StrEnum):
    """라프텔의 콘텐츠 등급을 나타냅니다."""
    ALL = "전체 이용가"
    TWELVE = "12세 이용가"
    FIFTEEN = "15세 이용가"
    NINETEEN = "19세 이용가"

class Weekdays(StrEnum):
    """일주일의 요일 이름을 나타냅니다."""
    MONDAY = "월요일"
    TUESDAY = "화요일"
    WEDNESDAY = "수요일"
    THURSDAY = "목요일"
    FRIDAY = "금요일"
    SATURDAY = "토요일"
    SUNDAY = "일요일"
    NONE = ""
