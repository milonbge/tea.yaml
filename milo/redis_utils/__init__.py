#!/usr/bin/env python

from cPickle import dumps, loads
from hashlib import sha1

from redis import StrictRedis

db = StrictRedis(db=6)

__all__ = ('memoize', )


def memoize(func, ttl=300):

    """
    Cache the results of a function that may
    be time-consuming or otherwise expensive.

    Default caching is for five minutes so oversights
    can't result in infinite caching (or a bloated
    Redis database).
    """

    def new_func(*args, **kwargs):

        #hash args & kwargs to make unique key
        arg_pickle = "{0}:{1}".format(dumps(args), dumps(kwargs))
        hash = sha1(arg_pickle).hexdigest()

        #make a key of the function name and the hashed arguments
        key = 'memoize_cache_{0}_{1}'.format(func.__name__, hash)

        #return cached value if it exists; otherwise do it live
        if db.exists(key):
            return loads(db.get(key))

        result = func(*args, **kwargs)
        db.setex(key, ttl, dumps(result))

        return result
    
    return new_func

if __name__ == '__main__':

    import time
    
    def foo(msg='bar'):
        time.sleep(1)
        return msg

    #memoize with a five-second timeout
    foo = memoize(foo, ttl=5)

    print foo()
    print foo('cat')



