import math
import asyncio
from itertools import islice


async def print_reminder(interval, future):
    while not future.done():
        print("This is a reminder.")
        await asyncio.sleep(interval)


def lucas():
    a = 2
    yield a
    b = 1
    while True:
        yield b
        a, b = b, a + b


async def is_prime(number):
    if number <= 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            break
        await asyncio.sleep(0)
    else:
        return True
    return False


async def print_results(iterable, async_function, task_name, future):
    for item in iterable:
        if await async_function(item):
            print("Found: %s in %s" % (item, task_name))
    future.set_result("Done!")


loop = asyncio.get_event_loop()
future = loop.create_future()
loop.create_task(print_reminder(3, future))
loop.create_task(print_results(islice(lucas(), 30, 40), is_prime, 'task1', future))
loop.run_until_complete(future)
