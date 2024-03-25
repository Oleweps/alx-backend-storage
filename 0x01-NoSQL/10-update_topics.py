#!/usr/bin/env python3
""" function that changes all topics of a school document based on the name
"""
from typing import List


def update_topics(mongo_collection,
                  name: str, topics: List[str]) -> None:
    """ changes all topics of a school document based on the name
        Args:
            mongo_collection: pymongo collection
            name: name of school to update
            topics: list of topics approached in school
    """

    mongo_collection.update_many({"name": name},
                                 {"$set": {"topics": topics}})
