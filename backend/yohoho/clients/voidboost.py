import httpx

from ..data_types import IframesOutput


async def get_iframes(kinopoisk_id: str) -> list[IframesOutput]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://voidboost.tv/embed/{kinopoisk_id}")
    response.raise_for_status()
    return [
        IframesOutput(
            source_name="voidboost",
            iframe_url=f"https://voidboost.tv/embed/{kinopoisk_id}",
        )
    ]
