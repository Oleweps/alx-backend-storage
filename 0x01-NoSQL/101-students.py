#!/usr/bin/env python3
""" Top students sorted by average score
"""


def top_students(mongo_collection):
    """ Get top students sorted by average score
        Args:
            mongo_collection: pymongo collection
        Return:
           list of all top students stored
    """

    students = list(mongo_collection.find())
    students_avg = {}

    for student in students:
        name = student.get("name")
        tmp = 0
        topics = student.get("topics")
        for topic in topics:
            tmp += topic.get("score")
        avg = tmp / len(topics)
        students_avg[name] = avg

    students_avg = dict(sorted(students_avg.items(),
                        key=lambda kv: (kv[1], kv[0]), reverse=True))

    new_dict = []
    for key, val in students_avg.items():
        for student in students:
            if key == student.get("name"):
                student["averageScore"] = val
                new_dict.append(student)
                break

    return new_dict
