#!/usr/bin/env python3
"""
A script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection, option=None):
    '''
    This prints log status
    '''
    items = {}

    if option:
        value = mongo_collection.count_documents({"method": option})
        print(f"\tmethod {option}: {value}")
        return

    result = mongo_collection.count_documents(items)
    print(f"{result} logs")
    print("Methods:")
    for method in METHODS:
        log_stats(mongo_collection, method)

    status_check = mongo_collection.count_documents({"path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    mongo_client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = mongo_client.logs.nginx
    log_stats(nginx_collection)
