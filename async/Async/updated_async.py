import time
import math
import asyncio


class Task(object):
    def __init__(self, generator):
        self.start = time.time()
        self.gen = generator
        self.total = None


class Scheduler(object):
    def __init__(self):
        self.ready_task = list()
        self.success_task = list()
        self.failed_task = list()

    def add_task(self, generator):
        task = Task(generator)
        self.ready_task.append(task)

    def run_to_completion(self):
        while self.ready_task:
            try:
                task = self.ready_task.pop(0)
                yielded = next(task.gen)
            except StopIteration:
                print("Task successfully finished.")
                task.total = time.time() - task.start
                self.success_task.append(task)
            except Exception as e:
                print("Task Failed: %s" % str(e))
                self.failed_task.append(task)
            else:
                assert yielded is None
                self.ready_task.append(task)


def print_reminder(message, interval):
    i = 0
    while True:
        print(message)
        yield from async_sleep(interval)
        i += 1


def async_sleep(interval):
    start = time.time()
    end = start + interval
    while True:
        yield
        if end <= time.time():
            break


def lucas():
    a = 2
    yield a
    b = 1
    while True:
        yield b
        a, b = b, a + b


def is_prime(number):
    if number <= 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            break
        yield from asyncio.sleep(0)
    else:
        return True
    return False


def print_results(iterable, async_function, task_name):
    for item in iterable:
        match = yield from async_function(item)
        if match:
            print("Found: %s in %s" % (item, task_name))


s = Scheduler()
s.add_task(print_reminder('async message', 3))
s.add_task(print_results(lucas(), is_prime, 'task1'))
s.run_to_completion()
