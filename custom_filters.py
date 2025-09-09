"""
Examples of custom filters
"""

from typing import Any

def custom_filter(data: list[Any]) -> bool:
    result = sum(filter(lambda i: isinstance(i, int) and i % 7 == 0, data))
    return result <= 83


if __name__ == '__main__':
    some_list = [7, 14, 28, 32, 32, 56]
    print(custom_filter(some_list))

    some_list = [7, 14, 28, 32, 32, '56']
    print(custom_filter(some_list))

    some_list = []
    print(custom_filter(some_list))
