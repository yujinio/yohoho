import httpx

from ..config import VIDEOCDN_TOKEN
from ..data_types import IframesOutput


async def get_iframes(kinopoisk_id: str) -> list[IframesOutput]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://videocdn.tv/api/short", params={"kinopoisk_id": kinopoisk_id, "api_token": VIDEOCDN_TOKEN}
        )
    response.raise_for_status()
    response_json = response.json()
    return [
        IframesOutput(
            source_name=f"videocdn {index + 1}",
            iframe_url=result["iframe_src"],
        )
        for index, result in enumerate(response_json["data"])
    ]
