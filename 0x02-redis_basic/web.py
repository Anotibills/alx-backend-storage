#!/usr/bin/env python3
"""
Script with requests module to obtain the HTML content of a particular URL
and returns it
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    '''
    This track how many times a particular URL was accessed in the key
    '''
    @wraps(method)
    def wrapper(url):
        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)

        if cached_data:
            return cached_data.decode("utf-8")

        count_key = f"count:{url}"
        html = method(url)

        store.incr(count_key)
        store.setex(cached_key, 10, html)  # Using setex for expiration
        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    '''
    This returns HTML content of a URL
    '''
    res = requests.get(url)
    return res.text
