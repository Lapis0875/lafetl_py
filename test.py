from asyncio import run
from laftel import LaftelAPI

async def items():
    api = LaftelAPI()
    async with api:
        res = [await api.items(41854), await api.items(16004)]   # 마슐: 신각자 후보 선발시험 편 / (더빙) 어떤 과학의 초전자포
        for anime in res:
            print(f"애니 제목: {anime.name}\n라프텔 평점: {anime.avg_rating}")

async def detail():
    api = LaftelAPI()
    async with api:
        res = await api.detail(41854)   # 마슐: 신각자 후보 선발시험 편
        print(f"애니 제목: {res.name}\n라프텔 평점: {res.avg_rating}")

async def search_all():
    api = LaftelAPI()
    async with api:
        res = await api.search_all("마슐")
        for i, anime in enumerate(res):
            print(f"애니 [{i}]")
            print(f"  애니 제목: {anime.name}\n  라프텔 id: {anime.id}")

async def main():
    print("api: items()")
    await items()
    
    print("api: search_all()")
    await search_all()

run(main())
