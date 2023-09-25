import httpx

from ..config import ALOHA_TOKEN
from ..data_types import IframesOutput


async def get_iframes(kinopoisk_id: str) -> list[IframesOutput]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.alloha.tv/", params={"kp": kinopoisk_id, "token": ALOHA_TOKEN})

    response.raise_for_status()
    response_json = response.json()

    if response_json.get("status") == "error":
        return []

    return [
        IframesOutput(
            source_name=f"aloha {index + 1}",
            iframe_url=result["iframe"],
            quality=result["quality"],
        )
        for index, result in enumerate(response_json["data"])
    ]
