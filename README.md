# Bisect helper

Python builtin `bisect` module can't be used directly with a list containing
slightly complex objects (e.g. dicts). This simple module provides a helper for
those cases. For example:
```python
items = [
    {"name": "John", "age": 24, "department": "HR"},
    {"name": "Annabel", "age": 52, "department": "production"},
    {"name": "Zoe", "age": 20, "department": "maintenance"},
]

items.sort(key=itemgetter("name"))
helper = BisectHelper(items, "name")
index = bisect.bisect(helper, "Michael")
```
