import asyncio
from asyncio import AbstractEventLoop
import signal
from typing import Set

# ------------------------------------------------------------------------------
import asyncio
import functools
import time
from typing import Any
from collections.abc import Awaitable, Callable


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


# ------------------------------------------------------------------------------


def cancel_tasks():
    print("Got a SIGINT!")
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f"Cancelling {len(tasks)} task(s).")
    [task.cancel() for task in tasks]


async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGINT, cancel_tasks)

    await delay(10)


asyncio.run(main())
