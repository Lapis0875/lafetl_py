from pydantic import BaseModel, NonNegativeInt, field_serializer, field_validator
from pydantic_core import Url

__all__ = ("CropRatio", "Image")

class CropRatio(BaseModel):
    x: NonNegativeInt
    y: NonNegativeInt
    width: NonNegativeInt
    height: NonNegativeInt

class Image(BaseModel):
    """라프텔 내부에서 이미지를 표현하는 객체."""
    crop_ratio: CropRatio       # 이 이미지를 자르기 위한 기준값.
    img_url: Url
    option_name: str
    
    @field_validator("crop_ratio", mode='before')
    @classmethod
    def validate_crop_ratio(cls, v: str) -> CropRatio:
        if isinstance(v, str):
            args = v.split(",")
            if len(args) != 4:
                raise ValueError(f"Invalid crop ratio value: {v}\n : 4 arguments must be provided.")
            return CropRatio.model_construct(x=int(args[0]), y=int(args[1]), width=int(args[2]), height=int(args[3]))
        return v
    
    @field_serializer("crop_ratio")
    @classmethod
    def serialize_crop_ratio(cls, cropRatio: CropRatio) -> str:
        return f"{cropRatio.x},{cropRatio.y},{cropRatio.width},{cropRatio.height}"
