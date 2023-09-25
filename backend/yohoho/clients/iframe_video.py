import httpx

from ..data_types import IframesOutput


async def get_iframes(kinopoisk_id: str) -> list[IframesOutput]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://iframe.video/api/v2/search", params={"kp": kinopoisk_id})
    response.raise_for_status()
    response_json = response.json()
    return [
        IframesOutput(
            source_name=f"iframe.video {index + 1}",
            iframe_url=result["path"],
        )
        for index, result in enumerate(response_json["results"])
    ]
