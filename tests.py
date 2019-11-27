import bisect
from collections import namedtuple
from operator import itemgetter

import pytest

from helper import BisectHelper


def test_simple():
    items = [{"name": "Kunegunda", "age": 42}]
    helper = BisectHelper(items, "name")
    assert helper[0] == items[0]["name"]


def test_access_path_walking():
    items = [{"company": {"department": {"building": [None, None, {"floor": [{"room": 42}]}]}}}]
    helper = BisectHelper(items, "company.department.building.2.floor.0.room")
    assert helper[0] == items[0]["company"]["department"]["building"][2]["floor"][0]["room"]


def test_access_path_mix_items_and_attrs():
    Point3d = namedtuple("Point3d", "x y z")
    items = [{"points": [Point3d(1, 0, -1)]}]
    helper = BisectHelper(items, "points.0.z")
    assert helper[0] == items[0]["points"][0].z


def test_throws():
    items = {"name": "Kunegunda", "age": 42}
    helper = BisectHelper(items, "height")
    with pytest.raises(LookupError):
        helper[0]


def test_simple_bisect():
    collection = [
        {"name": "Kunegunda", "age": 42},
        {"name": "Kaliksta", "age": 13},
        {"name": "Rozalinda", "age": 123},
    ]
    collection.sort(key=itemgetter("age"))
    helper = BisectHelper(collection, "age")

    assert bisect.bisect_left(helper, 39) == 1
