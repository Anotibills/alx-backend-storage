#!/usr/bin/env python3
"""
A script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_logs_stats():
    '''
    Connect to MongoDB
    '''
    client = MongoClient("mongodb://localhost:27017/")
    db = client["logs"]
    collection = db["nginx"]

    total_logs = collection.count_documents({})

    print(f"{total_logs} logs where "
          f"{total_logs} is the number of documents in this collection")

    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in http_methods:
        count = collection.count_documents({"method": method})
        print(f"\t{count} logs with method={method}")

    specific_logs_count = collection.count_documents({
        "method": "GET",
        "path": "/status"
    })

    print(f"{specific_logs_count} logs with method=GET and path=/status")


if __name__ == "__main__":
    nginx_logs_stats()
