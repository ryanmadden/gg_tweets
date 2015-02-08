# data = []
# with open('gg2013.json') as f:
#     for line in f:
#         data.append(json.loads(line))
#         print line
#         break

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
	count = 0

	filename_2015_mini = './gg15mini.json'
	filename_2015      = './goldenglobes2015.json'
	filename_2013      = './gg2013.json'
	wordset = preprocess.create_preprocess_wordset()
	
	with open(filename_2013, 'r') as f:
		for line in f:
			loaded = json.loads(line)
			for d in loaded:
				for key, value in d.iteritems():
					if key == 'text':
						lower_text  = value.lower()

						"""
							Preprocess and filter out unuseful tweets based on preprocess.txt
							Only do the expensive people parsing step if the tweet has any of the
							keywords we identify at the beginning
							Speedup of around ~5times
							
						"""
						if preprocess.filter_tweet(lower_text, wordset):

							# token_dict = text_to_token_dict(lower_text,STOP_WORDS,True)
							count +=1
							# print value
							# if any([True for tok in token_dict if tok in SOW]):
							"""This people dict step in NLTK is slow"""
							#people_dict = text_to_people_dict(text)
							# people_dict =  text_to_people_dict_naive_fast(text,FOW)

							# memorize_people_if_tokens_match(token_dict, people_dict, MEMORY, IMPORTANT_WORDS)

							# _trie_memorize_people_if_tokens_match(token_dict, people_dict, TRIE, IMPORTANT_WORDS)

	#pprint(MEMORY)
	#pprint(TRIE)
	# get_top_n_vals(MEMORY, 5)

	# trie_top_n_vals(TRIE, 5)
	# pprint(get_trie_top_n_vals(TRIE, 5))
	print count


if __name__ == "__main__":
	main()