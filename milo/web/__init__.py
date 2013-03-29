#!/usr/bin/env python

from datetime import timedelta
from redis import StrictRedis
import requests

HR_IN_SECS = int(timedelta(hours=1).total_seconds())

db = StrictRedis()

__all__ = ('polite_get',)

def polite_get(url):
    
    """
    Don't hammer the remote servers.
    
    1. They don't update that often anyway.
    2. We don't want to get throttled or banned.
    3. It's polite.
    """

    key = "url_cache::{0}".format(url)
    result = db.get(key)

    if result is None:
        
        page = requests.get(url)
        result = page.text
        db.setex(key, HR_IN_SECS, result)
        
    return result
