#!/usr/bin/env python3
"""
This is module on Redis
"""
import uuid
from functools import wraps
from typing import Callable, Union

import redis


def count_calls(method: Callable) -> Callable:
    '''
    This is the count for each method call
    '''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        This returns the original method's result
        '''
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    This stores the history of inputs and outputs
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        This takes input and output of each function call and retunrs output
        '''
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def replay(fn: Callable):
    '''
    This replays the history of calls
    '''
    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)
    n_calls = n_calls.decode('utf-8') if n_calls else 0

    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ":inputs", 0, -1)
    outs = r.lrange(f_name + ":outputs", 0, -1)

    for i, o in zip(ins, outs):
        i = i.decode('utf-8') if i else ""
        o = o.decode('utf-8') if o else ""
        print(f'{f_name}(*{i}) -> {o}')


class Cache:
    '''
    This is the class on cache
    '''

    def __init__(self) -> None:
        '''
        Initialise
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Ths stores data and returns the key
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float]:
        '''
        Uses get to return data
        '''
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        '''
        This returns the variable to a string
        '''
        variable = self._redis.get(key)
        return variable.decode("UTF-8") if variable else ""

    def get_int(self, key: str) -> int:
        '''
        This returns the variable to an integer
        '''
        variable = self._redis.get(key)
        try:
            return int(variable.decode("UTF-8")) if variable else 0
        except ValueError:
            return 0
