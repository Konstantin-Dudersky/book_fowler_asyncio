import asyncio
import aiohttp

# ------------------------------------------------------------------------------
import functools
import time
from typing import Any
from collections.abc import Awaitable, Callable

from aiohttp import ClientSession


async def delay(delay_seconds: int) -> int:
    print(f"sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)
    print(f"finished sleeping for {delay_seconds} second(s)")
    return delay_seconds


def async_timed():
    def wrapper(
        func: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[Any]]:
        @functools.wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            print(f"starting {func} with args {args} {kwargs}")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f"finished {func} in {total:.4f} second(s)")

        return wrapped

    return wrapper


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


# ------------------------------------------------------------------------------


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com" for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


asyncio.run(main())
