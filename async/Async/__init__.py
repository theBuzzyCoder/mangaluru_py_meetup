
import math
from itertools import islice


def fibonacci(number):
    i = 2
    a = 0
    b = 1
    fibonacci_series = [a, b]
    while i < number:
        a, b = b, a + b
        i += 1
        fibonacci_series.append(b)
    return fibonacci_series


def async_fibonacci():
    a = 0
    yield a
    b = 1
    while True:
        yield b
        a, b = b, a + b


def lucas(number):
    i, a, b = 2, 2, 1
    lucas_sequence = [a, b]
    while i < number:
        i += 1
        a, b = b, a + b
        lucas_sequence.append(b)


def async_lucas():
    a = 2
    yield a
    b = 1
    while True:
        yield b
        a, b = b, a + b


def async_get_all_odd_numbers():
    i = 1
    while True:
        yield i
        i += 2


def is_prime(number):
    if number < 2:
        return False
    for i in range(3, int(math.sqrt(number)) + 1):
        if number % i == 0:
            break
        yield
    else:
        return True
    return False


class Future(object):
    def __init__(self, generator):
        self.gen = generator
        self.output = None

    def resolve(self):
        return self.gen.next()


class Task(object):
    def __init__(self):
        self.ready_task = list()
        self.success_task = list()
        self.failed_task = list()
        self.suspended_task = list()

    def add_task(self, generator):
        future = Future(generator)
        self.ready_task.append(future)

    def resume_task(self):
        future = self.suspended_task.pop(0)
        self.ready_task.append(future)

    def run_to_complete(self):
        while self.ready_task:
            try:
                future = self.ready_task.pop(0)
                yielded = future.resolve()
            except StopIteration as e:
                future.output = e.value
                print("Task successfully finished. Output: %s" % e.value)
                self.success_task.append(future)
            except Exception as e:
                print("Task Failed: %s" % str(e))
                self.failed_task.append(future)
            else:
                assert yielded is None
                self.suspended_task.append(future)
                if (not self.ready_task) and self.suspended_task:
                    future = self.suspended_task.pop(0)
                    self.ready_task.append(future)
