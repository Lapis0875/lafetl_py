from asyncio import run
from laftel import LaftelAPI

async def main():
    api = LaftelAPI()
    async with api:
        res = await api.search_all("마슐")
        for i, anime in enumerate(res):
            print(f"애니 [{i}]")
            print(f"  애니 제목: {anime.name}\n  라프텔 id: {anime.id}")

run(main())
