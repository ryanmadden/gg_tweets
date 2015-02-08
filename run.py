import time
import timeit
import nltk
from nltk import word_tokenize
import json
import preprocess


"""
Timing decorator to monitor a function's duration
"""
def timeit(f):

    def timed(*args, **kw):
        start     = time.time()
        result    = f(*args, **kw)
        end       = time.time()

        print 'func:%r took: %2.4f sec' % (f.__name__, end-start)
        return result

    return timed


@timeit
def main():
	filename_2015_mini = './gg15mini.json'
	filename_2015      = './goldenglobes2015.json'
	filename_2013      = './gg2013.json'
	count = 0
	wordset = preprocess.create_preprocess_wordset()

	with open(filename_2013, 'r') as f:
		loaded = json.loads(f)
		for d in loaded:
			for key, value in d.iteritems():
				if key == 'text':
					lower_text  = value.lower()
					if preprocess.filter_tweet(lower_text, wordset):
						count +=1
	print count


if __name__ == "__main__":
	main()