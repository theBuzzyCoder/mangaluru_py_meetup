import math


def get_all_odd_numbers(limit):
    series = list()
    for i in range(1, limit, 2):
        series.append(i)
    return series


def is_prime(number):
    if number < 2:
        return False
    for i in range(3, int(math.sqrt(number)) + 1):
        if number % i == 0:
            break
    else:
        return True
    return False


for number in get_all_odd_numbers((2 ** 25) - 1):
    print(number)
