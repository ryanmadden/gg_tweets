import time
from nltk import word_tokenize
import json


def timeit(f):
    def timed(*args, **kw):
        start  = time.time()
        result = f(*args, **kw)
        end    = time.time()
        print 'func:%r took: %2.4f sec' % (f.__name__, te-ts)
        return result
    return timed


def filter_tweet(tweet, wordset):
	if any([True for word in word_tokenize(tweet) if word in wordset]):
		return True
	return False


def create_preprocess_wordset():
	wordlist = []
	with open('./preprocess.txt', 'r') as f:
		wordlist = f.read().replace('\n','').split(',')
		return set(wordlist)