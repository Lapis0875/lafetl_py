from pprint import pprint
from typing import Any, Final

import aiohttp

from .models import *

__all__ = ("LaftelAPI", )

laftel_header: Final[dict[str, Any]] = {"laftel": "Tejava"}
laftel_api_base: Final[str] = "https://laftel.net"

class LaftelAPI:
    _session: aiohttp.ClientSession

    def __init__(self) -> None:
        self._session = aiohttp.ClientSession(laftel_api_base)
    
    # Session Management
    
    def handle_session(self):
        if self._session.closed:
            self._session = aiohttp.ClientSession(laftel_api_base)
    
    async def close(self) -> None:
        """라프텔 API 세션을 닫습니다."""
        if not self._session.closed:
            await self._session.close()
    
    # Asynchronous Context Manager
    
    async def __aenter__(self) -> None:
        self.handle_session()
        
    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self._session.close()
    
    # Below methods should be used only in async context. Other behaviors can generate errors.
    
    async def detail(self, id: int) -> Anime:
        """라프텔의 애니메이션 정보를 가져옵니다.

        Args:
            id (int): 찾으려는 애니메이션의 id

        Returns:
            Anime: 애니메이션 객체.
        """
        self.handle_session()
        async with self._session as session:
            async with session.get(f"/api/v1.0/items/{id}/detail", headers=laftel_header) as response:
                resp_content = await response.json()
                return Anime(**resp_content)
    
    async def search(self, query: str, viewing_only: bool = True, offset: int = 0, size: int = 24) -> tuple[list[AnimeSearchResult], bool]:
        """라프텔의 애니메이션 정보를 검색합니다.

        Args:
            query (str): 검색어.
            viewing_only (bool): 감상 가능한 작품만 검색할지 여부. 기본값은 True.
            offset (int): 검색 시작할 작품의 위치. 기본값은 0.
            size (int): 한번에 검색할 작품의 개수. 기본값은 24.

        Returns:
            list[Anime]: 검색된 애니메이션 객체들의 배열.
            bool: 다음 페이지가 있는지 여부.
        """
        self.handle_session()
        async with self._session as session:
            res: list[PartialAnime] = []
            async with session.get(
                url="/api/search/v3/keyword/",
                headers=laftel_header,
                params={"keyword": query, "viewing_only": str(viewing_only).lower(), "offset": offset, "size": size}
            ) as response:
                resp_content = await response.json()
            for anime_json in resp_content["results"]:
                res.append(AnimeSearchResult(**anime_json))
                    
            return res, resp_content["next"] is not None

    async def search_all(self, query: str, viewing_only: bool = True, size: int = 24) -> list[AnimeSearchResult]:
        res: list[PartialAnime] = []
        offset: int = 0
        keep_query: bool = True
        while keep_query:
            arr, keep_query = await self.search(query, viewing_only, offset, size)
            res.extend(arr)
            offset += size
        
        return res