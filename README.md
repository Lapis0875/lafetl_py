# laftel.py

## 어떤 라이브러리인가요?

[라프텔](https://laftel.net) 이라는 애니메이션 스트리밍 서비스 상의 애니메이션 정보들을 조회하고 다루기 위한 ⚠️**비공식** api 래퍼입니다.
타 프로젝트를 진행하며 필요한 부분들만 우선적으로 구현하고 있습니다.

## 예제 코드

라이브러리를 쉽게 이용하기 위한 몇가지 예제 코드입니다. 문서화는 추후 진행할 예정입니다.

### 특정 id의 애니메이션 검색하기

라프텔 내부의 애니메이션 정보들은 id를 통해 특정할 수 있습니다.
LaftelAPI의 `detail` 메소드는 id를 인자로 받아, 해당 애니메이션 정보를 반환합니다.
현재 과거 api인 v1.0을 기준으로 구현되었으나, 현재 사용중인 api를 기준으로 구현을 다시 할 계획입니다.

```python
from asyncio import run
from laftel import LaftelAPI

async def main():
    api = LaftelAPI()
    async with api:
        res = await api.detail(41854)   # 마슐: 신각자 후보 선발시험 편
        print(f"애니 제목: {res.name}\n라프텔 평점: {res.avg_rating}")

run(main())
```

### 특정 키워드로 애니메이션 검색하기

간단하게, 특정 키워드로 검색한 결과를 얻는 코드는 아래와 같습니다.

```python
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
```

보다 상세하게, api 구현대로 검색할 수 있는 코드는 아래와 같습니다.
다만, 이미 LaftelAPI 객체의 `search_all` 메소드가 이를 구현하고 있으니 추가적인 구현이 필요하지 않다면 이를 사용하는걸 권장합니다.

```python
from asyncio import run
from laftel import LaftelAPI

async def main():
    api = LaftelAPI()
    async with api:
        item_left: bool = True
        offset: int = 0
        chunk_size: int = 5

        while item_left:
            res, item_left = await api.search("마슐", True, offset, chunk_size)
            for i, anime in enumerate(res):
                print(f"애니 [{i}]")
                print(f"  애니 제목: {anime.name}\n  라프텔 id: {anime.id}")
            if item_left:
                offset += chunk_size
run(main())
```
