import time


def timeit(callback):
    start = time.time()

    def wrapper(*args, **kwargs):
        data = callback(*args, **kwargs)
        end = time.time()
        print("%s took %.2f seconds" % (callback.__name__, end - start))
        return data
    return wrapper
