from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from .base import LaftelDBEntry

__all__ = ("MetaInfo", )

class MetaInfo(LaftelDBEntry):
    """라프텔 객체의 메타 정보를 나타냅니다."""
    item: NonNegativeInt
    is_viewing: bool
    rank: int | None
    point: NonNegativeInt
    cnt_short_review: NonNegativeInt
    is_avod: bool
    is_svod: bool
    subtitle_required: bool
    cnt_wish: NonNegativeInt
    cnt_view: NonNegativeInt
    cnt_go_episode: NonNegativeInt
    cnt_rec: NonNegativeInt
    male: NonNegativeInt
    female: NonNegativeInt
    point_for_new: NonNegativeInt
    extra_data: dict
    avg_rating: NonNegativeFloat
    cnt_eval: NonNegativeInt
    cnt_eval_05: NonNegativeInt
    cnt_eval_10: NonNegativeInt
    cnt_eval_15: NonNegativeInt
    cnt_eval_20: NonNegativeInt
    cnt_eval_25: NonNegativeInt
    cnt_eval_30: NonNegativeInt
    cnt_eval_35: NonNegativeInt
    cnt_eval_40: NonNegativeInt
    cnt_eval_45: NonNegativeInt
    cnt_eval_50: NonNegativeInt
    
    