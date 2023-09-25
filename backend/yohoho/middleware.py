import time

from litestar.datastructures import MutableScopeHeaders
from litestar.enums import ScopeType
from litestar.middleware import AbstractMiddleware
from litestar.types.asgi_types import Message, Receive, Scope, Send


class ProcessingTimeMiddleware(AbstractMiddleware):
    scopes = {ScopeType.HTTP}

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        start_time = time.time()

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableScopeHeaders.from_message(message=message)
                headers["X-Process-Time-Seconds"] = str(time.time() - start_time)
            await send(message)

        await self.app(scope, receive, send_wrapper)
