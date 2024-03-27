#!/usr/bin/env python3
""" test cache results function
"""
import redis
import time

get_page = __import__("web").get_page
client = redis.Redis()
start = time.perf_counter()

print(get_page("http://slowwly.robertomurray.co.uk"))
print(client.get("count:http://slowwly.robertomurray.co.uk"))
print("seconds = {}".format(time.perf_counter() - start))
