#!/usr/bin/env python

from datetime import timedelta
from redis import StrictRedis
import requests

TTL = int(timedelta(hours=1).total_seconds())

__all__ = ('polite_get',)

def polite_get(url, ttl=TTL, db=0, port=6379):

    """
    Don't hammer the remote servers.

    1. They don't update that often anyway.
    2. We don't want to get throttled or banned.
    3. It's polite.

    Accepts kwargs for ttl, db, and port; otherwise
    uses Redis defaults and a one-hour ttl.
    """

    db = StrictRedis(db=db, port=port)

    key = "url_cache::{0}".format(url)
    result = db.get(key)

    if result is None:

        page = requests.get(url)
        result = page.text
        db.setex(key, ttl, result.encode('utf-8'))

    else:
        result = result.decode('utf-8')

    return result
