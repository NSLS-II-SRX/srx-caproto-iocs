from __future__ import annotations

import datetime


def now(as_object=False):
    """A helper function to return ISO 8601 formatted datetime string."""
    _now = datetime.datetime.now()
    if as_object:
        return _now
    return _now.isoformat()
