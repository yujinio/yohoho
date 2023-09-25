import asyncio

from . import data_types
from .clients import aloha, apicollaps, apivb, bazon, iframe_video, kinopoisk, videocdn, voidboost


async def search(q: str) -> data_types.SearchOutput:
    return await kinopoisk.search(q)


async def get_iframes(kinopoisk_id: int) -> list[data_types.IframesOutput]:
    tasks = (
        aloha.get_iframes(kinopoisk_id),
        apicollaps.get_iframes(kinopoisk_id),
        apivb.get_iframes(kinopoisk_id),
        bazon.get_iframes(kinopoisk_id),
        iframe_video.get_iframes(kinopoisk_id),
        videocdn.get_iframes(kinopoisk_id),
        voidboost.get_iframes(kinopoisk_id),
    )
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [iframe for result in results if not isinstance(result, Exception) for iframe in result]
