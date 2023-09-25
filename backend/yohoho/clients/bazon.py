import httpx

from ..config import BAZON_TOKEN
from ..data_types import IframesOutput


async def get_iframes(kinopoisk_id: str) -> list[IframesOutput]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://bazon.cc/api/search", params={"kp": kinopoisk_id, "token": BAZON_TOKEN})
    response.raise_for_status()
    response_json = response.json()

    if "error" in response_json:
        return []

    return [
        IframesOutput(
            source_name=f"bazon {index + 1}",
            iframe_url=result["link"],
            quality=result["quality"],
        )
        for index, result in enumerate(response_json["results"])
    ]
