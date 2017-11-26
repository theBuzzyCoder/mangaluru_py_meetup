import math
import datetime
import asyncio


async def print_reminder(message, interval):
    while True:
        print(message + ' ' + str(datetime.datetime.now()))
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


async def print_results(iterable, async_function, task_name):
    for item in iterable:
        if await async_function(item):
            print("Found: %s in %s" % (item, task_name))


loop = asyncio.get_event_loop()
loop.create_task(print_reminder('async message', 3))
loop.create_task(print_results(lucas(), is_prime, 'task1'))
loop.run_forever()
