from pydantic import NonNegativeFloat, NonNegativeInt, field_validator, field_serializer
from pydantic_core import Url
from datetime import datetime

from .base import LaftelDBEntry, LaftelObject
from .enums import *
from .image import CropRatio
from .air_time import AirTime
from .tag import LaftelTag
from .person import *
from .production import Production
from .meta import MetaInfo
from .image import *
from .validators import Season, Year, Cours

__all__ = ("AnimationInfo", "AnimeSearchResult", "PartialAnime", "Anime")

class AnimationInfo(LaftelDBEntry):
    """라프텔의 애니메이션 정보를 나타냅니다."""
    air_year_quarter: Year
    audio_language: int | None
    cours: Cours | None                             # ~쿨 형식의 표현
    distributed_air_time: AirTime | None
    distributed_station: str | None
    is_dubbed: bool
    is_laftel_only: bool
    is_laftel_original: bool
    is_uncensored: bool
    item: NonNegativeInt
    medium: Medium
    original_air_time: AirTime | None
    original_station: str | None
    original_writer: list[PersonInfo]
    production: Production
    related_dubbed_item: NonNegativeInt | None
    scenario_writer: list[PersonInfo]                     # TODO: PersonInfo.job이 필드명과 동일하게끔 validation할 수 있을까?
    season: Season | None
    staff: list[NonNegativeInt]
    subtitle_language: NonNegativeInt | None
    
    @field_validator("distributed_air_time", "original_air_time", mode="before")
    @classmethod
    def validate_original_air_time(cls, v: str) -> AirTime | None:
        if isinstance(v, str) and v != "":
            if "|" in v:
                t, d = v.split(" | ")
                return AirTime.model_construct(time=t, day=d)
            elif v.endswith("일"):
                return AirTime.model_construct(time=None, day=v)
            else:
                return AirTime.model_construct(time=v, day="")
        return None

    @field_serializer("distributed_air_time", "original_air_time")
    @classmethod
    def serialize_original_air_time(cls, airTime: AirTime | None) -> str:
        if airTime is None:
            return None
        
        content: list[str] = ["", ""]
        if airTime.time is not None:
            content[0] = f"{airTime.time.hour}:{airTime.time.minute}"
        if airTime.day is not None:
            content[1] = str(airTime.day)
        if content[0]:
            if content[1]:
                return f"{content[0]} | {content[1]}"
            else:
                return content[0]
        else:
            return content[1]

class AnimeSearchResult(LaftelObject):
    """검색 api의 결과로 반환되는 일부 필드만 제공되는 애니메이션 객체를 나타냅니다."""
    avod_status: str
    content_rating: ContentRating
    cropped_img: CropRatio
    distributed_air_time: AirTime | None
    genres: list[str]
    home_cropped_img: CropRatio
    home_img: str
    images: list[Image]
    is_adult: bool
    is_avod: bool
    is_dubbed: bool
    is_episode_existed: bool
    is_expired: bool
    is_laftel_only: bool
    is_uncensored: bool
    is_viewing: bool
    latest_episode_created: datetime | None
    latest_published_datetime: datetime | None
    medium: Medium
    name: str
    
    @field_validator("cropped_img", "home_cropped_img", mode='before')
    @classmethod
    def validate_cropped_img(cls, v: str) -> CropRatio:
        if isinstance(v, str):
            args = v.split(",")
            if len(args) != 4:
                raise ValueError(f"Invalid crop ratio value: {v}\n : 4 arguments must be provided.")
            return CropRatio.model_construct(x=int(args[0]), y=int(args[1]), width=int(args[2]), height=int(args[3]))
        return None
    
    @field_serializer("cropped_img", "home_cropped_img")
    @classmethod
    def serialize_cropped_img(cls, cropRatio: CropRatio) -> str:
        return f"{cropRatio.x},{cropRatio.y},{cropRatio.width},{cropRatio.height}"
    
    @field_validator("distributed_air_time", mode="before")
    @classmethod
    def validate_original_air_time(cls, v: str) -> AirTime | None:
        if isinstance(v, str) and v != "":
            if "|" in v:
                t, d = v.split(" | ")
                return AirTime.model_construct(time=t, day=d)
            elif v.endswith("일"):
                return AirTime.model_construct(time=None, day=v)
            else:
                return AirTime.model_construct(time=v, day="")
        return None

    @field_serializer("distributed_air_time")
    @classmethod
    def serialize_original_air_time(cls, airTime: AirTime | None) -> str:
        if airTime is None:
            return None
        
        content: list[str] = ["", ""]
        if airTime.time is not None:
            content[0] = f"{airTime.time.hour}:{airTime.time.minute}"
        if airTime.day is not None:
            content[1] = str(airTime.day)
        if content[0]:
            if content[1]:
                return f"{content[0]} | {content[1]}"
            else:
                return content[0]
        else:
            return content[1]

class PartialAnime(LaftelObject):
    """연관 애니 및 시리즈 애니 등에서 일부 필드만 제공되는 애니메이션을 나타냅니다."""
    animation_info: AnimationInfo           # 이 애니메이션의 정보를 나타내는 JSON 데이터.
    author: list[PartialPersonInfo]         # 작가로 추정됨.
    avg_rating: NonNegativeFloat            # 이 애니메이션의 평균 평점.
    avod_status: str
    comics_info: dict                       # 이 애니메이션의 코믹스 정보를 나타내는 JSON 데이터.
    cropped_img: CropRatio                  # 이 애니메이션의 이미지를 자르는 기준값.
    illustrator: list[PartialPersonInfo]    # 일러스트레이터 정보로 추정됨.
    images: list[Image]                     # 이 애니메이션의 이미지들.
    img: Url                                # 이 애니메이션을 나타내는 이미지 url.
    is_adult: bool                          # 이 애니메이션이 성인용인지 여부.
    is_avod: bool
    is_expired: bool                        # 이 애니메이션의 판권이 만료되었는지 여부.
    is_viewing: bool                        # 이 애니메이션이 감상 가능한지 여부.
    latest_episode_created: datetime | None # 이 애니메이션의 마지막 에피소드의 생성일.
    latest_episode_num: int | None          # 이 애니메이션의 마지막 에피소드 번호.
    lightnovel_info: dict                   # 이 애니메이션의 라이트노벨 정보를 나타내는 JSON 데이터.
    name: str                               # 이 컨텐츠의 제목을 나타낸다.
    point: NonNegativeInt
    point_for_new: NonNegativeInt
    tag: list[LaftelTag]                    # 이 애니메이션의 태그들.
    type: str                               # 이 컨텐츠의 유형을 나타낸다.
    viewable: bool                          # 이 애니메이션이 라프텔에서 검색 가능한지 여부. false일 경우 검색 불가.
    webtoon_info: dict | None               # 이 애니메이션의 웹툰 정보를 나타내는 JSON 데이터 일 것으로 추정.
    
    @field_validator("cropped_img", mode='before')
    @classmethod
    def validate_cropped_img(cls, v: str) -> CropRatio:
        if isinstance(v, str):
            args = v.split(",")
            if len(args) != 4:
                raise ValueError(f"Invalid crop ratio value: {v}\n : 4 arguments must be provided.")
            return CropRatio.model_construct(x=int(args[0]), y=int(args[1]), width=int(args[2]), height=int(args[3]))
        return v
    
    @field_serializer("cropped_img")
    @classmethod
    def serialize_cropped_img(cls, cropRatio: CropRatio) -> str:
        return f"{cropRatio.x},{cropRatio.y},{cropRatio.width},{cropRatio.height}"

class Anime(LaftelDBEntry):
    """라프텔의 작품(애니메이션, 코믹스 등)을 나타냅니다."""
    animation_info: AnimationInfo       # 이 애니메이션의 정보를 나타내는 JSON 데이터.
    author: list[PartialPersonInfo]            # 작가로 추정됨.
    author_item: list[PersonInfo]       # 작가 정보로 추정됨.
    avg_rating: NonNegativeFloat        # 이 애니메이션의 평균 평점.
    awards: list[str]                   # 이 애니메이션이 라프텔 내에서 수상한 타이틀들.
    comics_info: dict                   # 이 애니메이션의 코믹스 정보를 나타내는 JSON 데이터.
    content: str                        # 이 애니메이션의 짧은 설명글.
    content_rating: ContentRating       # 이 애니메이션의 이용 등급.
    illustrator: list[PartialPersonInfo]       # 일러스트레이터 정보로 추정됨.
    img: Url                            # 이 애니메이션을 나타내는 이미지 url.
    is_adult: bool                      # 이 애니메이션이 성인용인지 여부.
    is_ending: bool                     # 이 애니메이션이 종영했는지 여부.
    lightnovel_info: dict               # 이 애니메이션의 라이트노벨 정보를 나타내는 JSON 데이터.
    main_tag: list[LaftelTag]           # 이 애니메이션의 주 태그들.
    mediamix_item: list                 # 미디어믹스 정보로 추정됨.
    meta_info: MetaInfo                 # 이 애니메이션의 메타 정보로 추정됨.
    name: str                           # 이 애니메이션의 제목을 나타낸다.
    related_item: list[PartialAnime]         # 이 애니메이션과 관련된 다른 애니메이션들.
    resolution: str | None              # 이 애니메이션의 해상도.
    series_item: list[PartialAnime]          # 이 애니메이션의 시리즈에 속하는 다른 애니메이션들.
    type: str                           # 이 애니메이션의 유형을 나타낸다.
    viewable: bool                      # 이 애니메이션이 라프텔에서 검색 가능한지 여부. false일 경우 검색 불가.
    webtoon_info: dict | None           # 이 애니메이션의 웹툰 정보를 나타내는 JSON 데이터 일 것으로 추정.
    
