#!/usr/bin/env python3
"""
A function that returns all students sorted by average score
"""
from pymongo import MongoClient


def top_students(mongo_collection):
    '''
    Returns all students sorted by average score.

    :param mongo_collection: pymongo collection object
    :return: List of students with names and average scores
    '''
    pipeline = [
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ]

    top_students_cursor = mongo_collection.aggregate(pipeline)
    top_students_list = list(top_students_cursor)

    return top_students_list


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["your_database_name"]
    collection = db["your_collection_name"]

    top_students_list = top_students(collection)

    for student in top_students_list:
        print(student)
