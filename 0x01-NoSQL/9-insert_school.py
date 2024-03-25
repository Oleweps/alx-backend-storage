#!/usr/bin/env python3
""" insert new document into collection
"""


def insert_school(mongo_collection, **kwargs) -> str:
    """ Insert new document into collection
        Args:
            mongo_collection: pymongo collection
            Kwargs: key value pairs
        Return:
            new document _id
    """

    return mongo_collection.insert_one(kwargs).inserted_id


if __name__ == "__main__":
    """ main """
