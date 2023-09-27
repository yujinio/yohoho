from litestar import Litestar, MediaType, Request, Response, status_codes
from litestar.config.cors import CORSConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.openapi import OpenAPIConfig
from litestar.stores import memory, redis

from . import config
from .api import API
from .middleware import ProcessingTimeMiddleware


def report_all_errors(request: Request, exc: Exception) -> Response:
    """Default handler for all exceptions."""
    return Response(
        media_type=MediaType.JSON,
        content={"detail": getattr(exc, "detail", str(exc))},
        status_code=getattr(exc, "status_code", status_codes.HTTP_500_INTERNAL_SERVER_ERROR),
    )


def create_app() -> Litestar:
    if config.SERVER_CACHE_STORE_URL:
        root_store = redis.RedisStore.with_client(url=config.SERVER_CACHE_STORE_URL)
        response_cache_store = root_store.with_namespace("response_cache")
        rate_limit_store = root_store.with_namespace("rate_limit")
    else:
        root_store = memory.MemoryStore()
        response_cache_store = memory.MemoryStore()
        rate_limit_store = memory.MemoryStore()

    rate_limit_config = RateLimitConfig(rate_limit=("second", 5))

    return Litestar(
        route_handlers=(API,),
        exception_handlers={Exception: report_all_errors},
        middleware=(
            ProcessingTimeMiddleware,
            rate_limit_config.middleware,
        ),
        openapi_config=OpenAPIConfig(title="Yohoho API", version="0.1.0"),
        stores={"root": root_store, "response_cache": response_cache_store, "rate_limit": rate_limit_store},
        response_cache_config=ResponseCacheConfig(
            store=response_cache_store, default_expiration=config.SERVER_CACHE_EXPIRE_SECONDS
        ),
        cors_config=CORSConfig(allow_origins=[config.FRONTEND_URL]),
    )
