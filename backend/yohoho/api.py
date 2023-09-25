from litestar import get, status_codes
from litestar.controller import Controller

from . import controller, data_types
from .config import SERVER_CACHE_IFRAMES_EXPIRE_SECONDS, SERVER_CACHE_SEARCH_EXPIRE_SECONDS


class API(Controller):
    path = "/api"

    @get("/search", status_code=status_codes.HTTP_200_OK, cache=SERVER_CACHE_SEARCH_EXPIRE_SECONDS)
    async def search(self, q: str) -> data_types.SearchOutput:
        return await controller.search(q)

    @get("/iframes", status_code=status_codes.HTTP_200_OK, cache=SERVER_CACHE_IFRAMES_EXPIRE_SECONDS)
    async def iframes(self, kinopoisk_id: int) -> list[data_types.IframesOutput]:
        return await controller.get_iframes(kinopoisk_id)
