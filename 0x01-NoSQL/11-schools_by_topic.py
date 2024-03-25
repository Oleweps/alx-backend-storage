#!/usr/bin/env python3
""" Get list of schools having a specific topic
"""
from typing import List


def schools_by_topic(mongo_collection,
                     topic: str) -> List[dict]:
    """ Get list of schools with specific topic
        Args:
            mongo_collection: pymongo collection
            topic: name of topic
        Return:
             list of schools having a specific topic
    """

    schools = list(mongo_collection.find())
    schools_with_topic = []

    for school in schools:
        if not school.get("topics"):
            continue
        if topic in school.get("topics"):
            schools_with_topic.append(school)

    return schools_with_topic
