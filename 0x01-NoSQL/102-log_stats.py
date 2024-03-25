#!/usr/bin/env python3
""" script that provides some stats
    about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient
from typing import List, Mapping, Any

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    http_methods: List = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    request_count: Mapping[str, int] = {}
    ip_addresses: Mapping[str, int] = {}
    status_check: int = 0

    for method in http_methods:
        request_count[method] = 0

    nginx_logs: List[Mapping[str, Any]] = list(nginx_collection.find())
    for log in nginx_logs:
        method = log.get('method')
        if method is not None and method.upper() in http_methods:
            request_count[method.upper()] += 1

        if method == "GET" and log.get("path") == "/status":
            status_check += 1

        # keep track of ip addresses
        ip_addresses[log.get("ip")] = 0

    print("{} logs".format(len(nginx_logs)))

    print("Methods:")
    for method, count in request_count.items():
        print("\tmethod {}: {}".format(method, count))

    print("{} status check".format(status_check))

    for log in nginx_logs:
        # update occurence
        ip_addresses[log.get("ip")] += 1

    ip_addresses = dict(sorted(ip_addresses.items(),
                        key=lambda kv: (kv[1], kv[0]), reverse=True))
    count = 0
    print("IPs:")
    for ip, value in ip_addresses.items():
        if count == 10:
            break
        print("\t{}: {}".format(ip, value))
        count += 1
