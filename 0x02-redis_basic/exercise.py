#!/usr/bin/env python3
"""
Writing strings to Redis store
"""
from functools import wraps
import redis
from typing import Union, Callable, Optional, Any
import uuid


def count_calls(method: Callable) -> Callable:
    """ count number of calls made by Cache class
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """ wrapper function that increaments
            the number of method calls.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ decorator to store the history of
        inputs and outputs for a particular function
    """
    input_data = method.__qualname__ + ":inputs"
    output_data = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """ wrapper function """

        self._redis.rpush(input_data, str(args))
        return_val = method(self, *args, **kwargs)
        self._redis.rpush(output_data, return_val)

        return return_val

    return wrapper


class Cache:
    """
      Class defination
    """
    def __init__(self):
        """
        Initialize class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store data in redis storage and return string
            Args:
                data: data to store
            Return:
                string representing key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """ get value by key
            Args:
                key: key to find value
                fn: comversion function
            Return:
                any type
        """
        if fn:
            return fn(self._redis.get(key))

        return self._redis.get(key)

    def get_str(self, val) -> str:
        """ convert bytes to string
            Args:
                val: value to convert to string
            Return:
                value as string
        """
        return val.decode("utf-8")

    def get_int(self, val) -> int:
        """ convert bytes to int
            Args:
                val: value to convert to int
            Return:
                value as integer
        """
        return int(val.decode("utf-8"))


def replay(method: Callable) -> None:
    """ function to display the history
        of calls of a particular function.
        Args:
            method_name: name of key
    """
    client = redis.Redis()

    method_name = method.__qualname__

    inputs = client.lrange("{}:inputs".format(method_name), 0, -1)
    outputs = client.lrange("{}:outputs".format(method_name), 0, -1)

    merged = dict(zip(inputs, outputs))

    print("{} was called {} times:".format(method_name, len(merged)))

    for key, val in merged.items():
        input_d = key.decode("utf-8")
        output = val.decode("utf-8")
        print("{}(*{}) -> {}".format(method_name, input_d, output))
