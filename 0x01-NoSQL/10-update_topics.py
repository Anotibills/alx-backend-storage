#!/usr/bin/env python3
"""
A function that changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    '''
    This returns updates topics of a school document based on the name
    '''
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
    return result.modified_count
