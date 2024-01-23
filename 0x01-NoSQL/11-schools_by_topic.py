#!/usr/bin/env python3
"""
A function that returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    '''
    This returns the list of schools having a specific topic
    '''
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
