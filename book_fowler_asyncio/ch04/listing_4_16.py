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
async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status


# ------------------------------------------------------------------------------


async def main():
    async with aiohttp.ClientSession() as session:
        api_a = fetch_status(session, "https://www.example.com")
        api_b = fetch_status(session, "https://www.example.com", delay=2)

        done, pending = await asyncio.wait([api_a, api_b], timeout=1)

        for task in pending:
            if task is api_b:
                print("API B too slow, cancelling")
                task.cancel()


asyncio.run(main())
