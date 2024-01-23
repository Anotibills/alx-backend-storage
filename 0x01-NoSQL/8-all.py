#!/usr/bin/env python3
"""
A function that lists all documents in a collection
"""


def list_all(mongo_collection):
    '''
    This returns list all documents in a MongoDB collection
    '''
    documents = list(mongo_collection.find())
    return documents
