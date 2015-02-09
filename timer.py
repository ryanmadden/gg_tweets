import time

def timeit(f):
    def timed(*args, **kw):
        start     = time.time()
        result    = f(*args, **kw)
        end       = time.time()
        print 'func:%r took: %2.4f sec' % (f.__name__, end-start)
        return result
    return timed