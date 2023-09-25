import httpx

from ..config import APIVB_TOKEN
from ..data_types import IframesOutput


async def get_iframes(kinopoisk_id: str) -> list[IframesOutput]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://apivb.info/api/videos.json", params={"id_kp": kinopoisk_id, "token": APIVB_TOKEN}
        )
    response.raise_for_status()
    response_json = response.json()
    return [
        IframesOutput(
            source_name=f"hdvb {index + 1}",
            iframe_url=result["iframe_url"],
            quality=result["quality"],
        )
        for index, result in enumerate(response_json)
    ]
