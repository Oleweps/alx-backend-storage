#!/usr/bin/env python3
""" module to list all documents in collection
"""


def list_all(mongo_collection):
    """ lists all documents in a collection
        Args:
             mongo_collection: mongo collection
        Return:
           list of documents
    """
    documents = list(mongo_collection.find())

    if len(documents) == 0:
        return []

    return documents


if __name__ == "__main__":
    """ main """
