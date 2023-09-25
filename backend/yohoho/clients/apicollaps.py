import httpx

from ..config import APICOLLAPS_TOKEN
from ..data_types import IframesOutput


async def get_iframes(kinopoisk_id: str) -> list[IframesOutput]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apicollaps.cc/list", params={"kinopoisk_id": kinopoisk_id, "token": APICOLLAPS_TOKEN}
        )
    response.raise_for_status()
    response_json = response.json()
    return [
        IframesOutput(
            source_name=f"apicollaps {index + 1}",
            iframe_url=result["iframe_url"],
            quality=result["quality"],
        )
        for index, result in enumerate(response_json["results"])
    ]
