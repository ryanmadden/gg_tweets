import time
import json
from nltk import word_tokenize


def timeit(f):
    def timed(*args, **kw):
        start     = time.time()
        result    = f(*args, **kw)
        end       = time.time()
        print 'func:%r took: %2.4f sec' % (f.__name__, end-start)
        return result

    return timed



def find_names(tweet):
	pass



def determine_results(hosts, presenters, nominees):
	pass



@timeit
def main():
	f_2015_mini = './gg15mini.json'
	f_2015      = './goldenglobes2015.json'
	f_2013      = './gg2013.json'

	host_filters      = ["host", "hosting", "hosts", "hosted"]
	presenter_filters = ["presented", "presenting", "presenter", "presenters"]
	award_names = [] #TODO

	hosts      = []
	presenters = {}
	nominees   = {}

	with open(f_2013, 'r') as f:
		tweets = map(json.loads, f)[0]

		for tweet in tweets:
			text  = tweet['text']
			names = ""

			if filt in text for filt in host_filters:
				names = find_names(text)
				hosts.extend(names)

			if award in text for award in award_names:
				if not names:
					names = find_names(text)
				nominees[award].extend(names)

				if filt in text for filt in presenter_filters:
					presenters[award].extend(names)





if __name__ == "__main__":
	main()