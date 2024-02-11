from datetime import time

from pydantic import BaseModel, field_validator

from .enums import Weekdays

__all__ = ("AirTime", )


class AirTime(BaseModel):
    time: time | None
    day: Weekdays
    
    @field_validator("time", mode="before")
    @classmethod
    def validate_time(cls, v: str) -> time:
        if isinstance(v, str):
            return time(*v.split(":"))
        return v
